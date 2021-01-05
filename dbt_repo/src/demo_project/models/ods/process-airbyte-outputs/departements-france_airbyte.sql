-- {{ config(materialized='table', schema='ods') }}


WITH departementsfrance_raw_airbyte AS (
    SELECT
        ab_id AS id,
        emitted_at,
        (data::json->>'code_departement')::TEXT AS code_departement,
        (data::json->>'nom_departement')::TEXT AS nom_departement,
        (data::json->>'code_region')::TEXT AS code_region,
        (data::json->>'nom_region')::TEXT AS nom_region
        
    FROM {{ source('stg', 'departements-france_stg') }}
)

SELECT
    code_departement,
    nom_departement,
    code_region,
    nom_region
FROM departementsfrance_raw_airbyte