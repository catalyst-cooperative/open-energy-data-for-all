---
title: "Plotting"
teaching: 0
exercises: 0
---


:::: questions

- How can I make data more legible, so that I can see what it is doing?
- How can I use plotting to speed up my debugging process?

::::

:::: objectives

- TBD

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

- _Motivate the example: what problem are we trying to solve?_
- _What data are we starting with?_
- _Where do we want to end up when we're done?_

## Exploratory data analysis

- _What data are we starting with?_
- _What threads can we pull that will get us closer to our goal?_

### [First debugging scenario]

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
