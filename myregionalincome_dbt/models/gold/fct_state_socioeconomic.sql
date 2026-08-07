select
    h.state,
    ds.state_code,
    ds.region,
    h.year,
    p.population_thousands,
    h.income_mean,
    h.income_median,
    h.poverty_rate,
    h.gini,
    c.avg_annual_cpi,
    round(h.income_mean / (c.avg_annual_cpi / 100), 2) as real_income_mean
from {{ ref('silver_hies_state') }} h
left join {{ ref('silver_population_state') }} p
    on h.state = p.state and h.year = p.year
inner join {{ ref('silver_cpi_state') }} c
    on h.state = c.state and h.year = c.year
left join {{ ref('dim_state') }} ds
    on h.state = ds.state