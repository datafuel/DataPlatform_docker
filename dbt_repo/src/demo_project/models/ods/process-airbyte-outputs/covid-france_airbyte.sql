-- {{ config(materialized='table', schema='ods') }}

WITH covidfrance_raw_airbyte AS (
    SELECT
        emitted_at,
        ab_id as id,
        (data::json->>'dc')::INTEGER AS nb_deces,
        (data::json->>'dep')::TEXT AS departement,
        (data::json->>'rad')::INTEGER AS nb_retours_au_domicile,
        (data::json->>'rea')::INTEGER AS nb_reanimations,
        (data::json->>'hosp')::INTEGER AS nb_hospitalisations,
        (data::json->>'jour')::DATE AS date_notification,
        (data::json->>'sexe')::INTEGER AS sexe
        
    FROM {{ source('stg', 'covid-france_stg') }}
)

SELECT
    id,
    departement,
    (CASE
        WHEN sexe = 1 THEN 'Hommes'
        WHEN sexe = 2 THEN 'Femmes'
    END)::TEXT AS sexe,
    date_notification,
    nb_hospitalisations,
    nb_reanimations,
    nb_retours_au_domicile,
    nb_deces
FROM covidfrance_raw_airbyte
WHERE sexe <> 0



