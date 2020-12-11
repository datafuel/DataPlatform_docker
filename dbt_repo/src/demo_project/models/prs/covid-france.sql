-- {{ config(materialized='view', schema='prs') }}
select
    nb_deces,
    departement,
    nb_retours_au_domicile,
    nb_reanimations,
    nb_hospitalisations,
    date_notification,
    sexe
    
from {{ref('covid-france_ods')}}