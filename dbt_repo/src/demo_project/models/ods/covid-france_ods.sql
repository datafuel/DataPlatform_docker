-- {{ config(materialized='table', schema='ods') }}
select
    ab_id as id,
    emitted_at,
    data::json->'dc' as nb_deces,
    data::json->'dep' as departement,
    data::json->'rad' as nb_retours_au_domicile,
    data::json->'rea' as nb_reanimations,
    data::json->'hosp' as nb_hospitalisations,
    data::json->'jour' as date_notification,
    data::json->'sexe' as sexe
    
from {{ source('stg', 'covid-france_stg') }}