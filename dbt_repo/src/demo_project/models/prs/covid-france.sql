-- {{ config(materialized='view', schema='prs') }}

SELECT 
    Date_Notification,
    Region,
    Departement,
    Sexe,
    Nb_Reanimations,
    Nb_Hospitalisations,
    Nb_Retours_au_Domicile,
    Nb_Deces
FROM {{ref('covid-france_ods')}}