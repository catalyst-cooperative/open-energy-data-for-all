---
title: "Troubleshooting Toolbox"
teaching: 0
exercises: 0
---


:::: questions

- Well that didn't work. What now?
- How can I make data more legible, so that I can see what's going on?
- How can I speed up my debugging process?

::::

:::: objectives

- TBD

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

- _Motivate the example: what problem are we trying to solve?_
  - Tentative: connecting CEMS emissions to EIA generation & generator attributes
- _What data are we starting with?_
- _Where do we want to end up when we're done?_

## Exploratory data analysis

- _What data are we starting with?_
- _What threads can we pull that will get us closer to our goal?_


### What can we match to EPA CEMS?

epacems: `core_epacems__hourly_emissions`

which is huge, so let's filter down to 2022 in CO

eia930: `core_eia930__hourly_net_generation_by_energy_source`, ~2022, ...what BAs are in CO?

eia861: `core_eia861__assn_balancing_authority`, CO gives us ids, but we need codes to filter 930

eia861: `core_eia861__yearly_balancing_authority` maps ids to codes

Now we can match emissions to generation by energy source:

```python
epacems.info()
```
```output
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 582504 entries, 0 to 582503
Data columns (total 16 columns):
 #   Column                     Non-Null Count   Dtype         
---  ------                     --------------   -----         
 0   plant_id_eia               582504 non-null  int32         
 1   plant_id_epa               582504 non-null  int32         
 2   emissions_unit_id_epa      582504 non-null  object        
 3   operating_datetime_utc     582504 non-null  datetime64[ms]
 4   year                       582504 non-null  int32         
 5   state                      582504 non-null  category      
 6   operating_time_hours       582504 non-null  float32       
 7   gross_load_mw              252664 non-null  float32       
 8   heat_content_mmbtu         252664 non-null  float32       
 9   steam_load_1000_lbs        0 non-null       float32       
 10  so2_mass_lbs               252664 non-null  float32       
 11  so2_mass_measurement_code  252664 non-null  category      
 12  nox_mass_lbs               252663 non-null  float32       
 13  nox_mass_measurement_code  252663 non-null  category      
 14  co2_mass_tons              252664 non-null  float32       
 15  co2_mass_measurement_code  252664 non-null  category      
dtypes: category(4), datetime64[ms](1), float32(7), int32(3), object(1)
memory usage: 33.3+ MB
```

```python
eia930.info()
```
```output
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1171331 entries, 0 to 1171330
Data columns (total 6 columns):
 #   Column                        Non-Null Count    Dtype         
---  ------                        --------------    -----         
 0   datetime_utc                  1171331 non-null  datetime64[ms]
 1   balancing_authority_code_eia  1171331 non-null  object        
 2   generation_energy_source      1171331 non-null  category      
 3   net_generation_reported_mwh   343374 non-null   float32       
 4   net_generation_adjusted_mwh   343376 non-null   float32       
 5   net_generation_imputed_mwh    6 non-null        float32       
dtypes: category(1), datetime64[ms](1), float32(3), object(1)
memory usage: 32.4+ MB
```

### Initial look

```python
(
    eia930
    .sort_values(by=["datetime_utc",]) # without this the result is a mess
    .groupby(["datetime_utc"], observed=True)
    .net_generation_reported_mwh
    .sum()
    .resample("24h").sum() # optional daily sum
    .plot()
)
```

Fine, 1-year time series showing piles of cooling in summer and a little bit of heating in winter

```python
(
    epacems
    .sort_values(by="operating_datetime_utc") # same deal, mess
    .groupby("operating_datetime_utc")
    [["gross_load_mw","heat_content_mmbtu","so2_mass_lbs","nox_mass_lbs","co2_mass_tons"]]
    .sum()
    .drop(columns="heat_content_mmbtu") # big difference in scale
    .resample("24h").sum() # optional daily sum
    .plot()
)
```

Fine, 1-year time series showing piles of emissions in summer and a lesser amount in winter

```python
plt.rcParams['figure.figsize'] = [12, 7] # adjust until subplots are legible
for i, ci in enumerate(["heat_content_mmbtu","co2_mass_tons","so2_mass_lbs","nox_mass_lbs"]):
    epacems_sum_all_plants.plot(
        x="gross_load_mw", 
        y=ci, 
        kind="hexbin", # scatter plot hides data density when points are close together
        ax=plt.subplot(2,2,i+1) # without this we get four separate plots
    )
```

Emissions proportional to load; heat and co2 cleanly, so2 and nox with more spread. nox has a suggestion of superposition at the low end.

### Does the match actually matter?

Emissions by energy source?

```python
merged ={}
for key,group in eia930_by_energy_source:
    merged[key] = group.merge(epacems_sum_all_plants, left_on="datetime_utc", right_on="operating_datetime_utc")
    #print(merged[key]) # for verifying the merge is right
    if merged[key].net_generation_reported_mwh.max()<1: continue # add after seeing tons of energy sources aren't usefully reported yet
    plt.figure() # add after removing the break, otherwise everything gets superimposed
    for i,ci in enumerate(["heat_content_mmbtu","co2_mass_tons","so2_mass_lbs","nox_mass_lbs"]): # copy and paste this loop from the epacems plot
        (
            merged[key]
            .plot(
                x="net_generation_reported_mwh", # not precisely the same as load, but our closest source-specific equivalent
                y=ci,
                kind="hexbin", 
                ax=plt.subplot(2,2,i+1)
            )
        )
    plt.suptitle(key)
    #break # just handle coal while getting started
```

Emissions increase with coal and gas generation, as expected

Also increase with hydro and maybe nuclear too, which is odd. maybe those are times when demand is generally high? 

But also hydro and nuclear have some weird gaps/bands, what's up with that

Emissions _decrease_ with wind generation, which feels neat; maybe indicating that on very windy days other sources shut down.

### Gaps and bands

```python
merged["hydro"]['netgen_p'] = (
    merged["hydro"]
    .net_generation_reported_mwh
    .rank(pct=True)
)
(
    merged["hydro"]
    .sort_values(by="net_generation_reported_mwh")
    .plot(x="net_generation_reported_mwh", y="netgen_p", title="hydro netgen cdf")
)
```

not terrifically satisfying, though we do see the two vertical regions at just-under-1000 and ~1500.

the nuclear version is pretty wild though

```python
for ci in ["hydro","nuclear"]:
    merged[ci]['netgen_p'] = (
        merged[ci]
        .net_generation_reported_mwh
        .rank(pct=True)
    )
    (
        merged[ci]
        .sort_values(by="net_generation_reported_mwh")
        .plot(x="net_generation_reported_mwh", y="netgen_p", title=f"{ci} netgen cdf")
    )
```

what is it about nuclear that makes it so easy/common to provide such distinct mwh rates?


## Data transformations

- _What are the basic steps of the data cleaning & processing pipeline that we need?_
- _How can we string them together in a way that still gives us opportunities to inspect intermediate results when something goes wrong?_

### [Second debugging scenario]

### [Third debugging scenario]

## Conclusions

- _TBD_


## Module development slush pile

### EDA

```python
df = pd.read_parquet("https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/nightly/out_eia923__generation_fuel_combined.parquet")
```

Remind ourselves what the data look like.

Key columns:
- independent variables: `report_date`
- grouping variables:
  - `plant_id_eia`
  - `energy_source*`
  - `fuel_type*`
  - `prime_mover*`
- dependent variables:
  - `fuel_consumed*`
  - `net_generation*`

#### General trends?

```python
df.plot("report_date","net_generation_mwh", kind="scatter")
```
[big indistinguishable blue mass]

Uhh not useful.

refinement:
```python
tbd
```

```python
len(df.groupby("plant_id_eia").groups)
```
```output
14565
```
oof that's a lotta series lines if we wanted one per plant.

```python
cats = ["plant_id_eia","energy_source_code","fuel_type_code_pudl","fuel_type_code_agg","prime_mover_code"]
for c in cats:
    print(f"{c}: {len(df.groupby(c, observed=True).groups)}")
```
```outputs
plant_id_eia: 14565
energy_source_code: 39
fuel_type_code_pudl: 8
fuel_type_code_agg: 17
prime_mover_code: 19
```

```python
for mover, data in df.sort_values(by="report_date").groupby("prime_mover_code"):
    data.plot(x="report_date",y="fuel_consumed_mmbtu",label=mover,kind="scatter")
```


```python
axs = (df[["fuel_type_code_pudl","net_generation_mwh"]]
 .reset_index(level="report_date")
 .groupby(["fuel_type_code_pudl","report_date"], observed=True)
 .mean()
 .reset_index(level="fuel_type_code_pudl")
 .groupby("fuel_type_code_pudl", observed=True)
 .plot(ax = plt.gca(), ylabel="net generation mwh")
)
axs.iloc[0].legend(labels=axs.reset_index().fuel_type_code_pudl)
```

#### Compliance?

```python
df.groupby("plant_id_eia").size().plot(linestyle="", marker='.')
```

Ooh interesting. Are the gaps significant? Are the heads and tails?

refinement:

```python
ax = df.groupby("plant_id_eia").size().sort_values(ascending=False).plot(kind='bar')
ax.get_xaxis().set_visible(False)
```

That x axis is gross and not helping, drop it



::::::::::::::::::::::::::::::::::::: keypoints

- placeholder

::::::::::::::::::::::::::::::::::::::::::::::::
