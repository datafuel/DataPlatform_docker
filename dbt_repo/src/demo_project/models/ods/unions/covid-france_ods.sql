-- {{ config(materialized='table', schema='ods') }}

WITH covidfrance_unioned_departements AS(
    SELECT
        d.nom_departement AS Departement,
        d.nom_region AS Region,
        c.sexe AS Sexe,
        c.nb_reanimations AS Nb_Reanimations,
        c.nb_hospitalisations AS Nb_Hospitalisations,
        c.nb_retours_au_domicile AS Nb_Retours_au_Domicile,
        c.nb_deces AS Nb_Deces,
        c.date_notification AS Date_Notification
        
    FROM {{ref('covid-france_airbyte')}} c

    JOIN {{ref('departements-france_airbyte')}} d 
        ON c.departement = d.code_departement
)

SELECT
    Date_Notification,
    Region,
    Departement,
    Sexe,
    Nb_Reanimations,
    Nb_Hospitalisations,
    Nb_Retours_au_Domicile,
    Nb_Deces
FROM covidfrance_unioned_departements