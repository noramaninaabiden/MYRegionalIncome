select
    state,
    extract(year from date) as year,
    gini,
    poverty as poverty_rate,
    income_mean,
    income_median,
    expenditure_mean
from {{ source('bronze', 'hies_state') }}