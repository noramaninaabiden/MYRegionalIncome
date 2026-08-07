select
    state,
    extract(year from date) as year,
    population as population_thousands
from {{ source('bronze', 'population_state') }}
where age = 'overall_age'
  and sex = 'overall_sex'
  and ethnicity = 'overall_ethnicity'