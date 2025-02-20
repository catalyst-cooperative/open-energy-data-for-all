---
title: "Plotting"
teaching: 0
exercises: 0
---



:::: questions 

- How can I get to know a data set that is new to me?
- How can I quickly evaluate data for outliers?
- How can I quickly identify patterns in data?
- How can I use plotting to speed up my debugging process?
- 

::::

:::: objectives

- Use plotting, grouping, and summation features of `pandas` to transform and display data as part of the exploratory data analysis and development phases of a project.
- 

::::::::::::::::::::::::::::::::::::::::::::::::

## Micro-objectives

- pd.DataFrame.plot()
  - pd.DataFrame.plot(kind='scatter')
  - pd.DataFrame.plot(kind='bar')
  - pd.DataFrame.plot(color=)
- pd.DataFrame.groupby()
  - pd.DataFrame.groupby().size()
  - pd.DataFrame.groupby().sum()
- pd.DataFrame.sort_values()

## Slush pile

### EDA

```python
df = pd.read_parquet("https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/nightly/core_eia923__monthly_generation_fuel.parquet")
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
^^^ ideally put these in a single axis; can fail out to plt if needed

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

