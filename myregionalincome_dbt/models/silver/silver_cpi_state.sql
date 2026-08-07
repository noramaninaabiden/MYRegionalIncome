select
    state,
    extract(year from date) as year,
    avg("index") as avg_annual_cpi
from {{ source('bronze', 'cpi_state') }}
where division = 'overall'
group by state, extract(year from date)