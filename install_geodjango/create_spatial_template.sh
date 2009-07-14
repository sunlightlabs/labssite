createdb -E UTF8 template_postgis # Creating the template spatial database.
createlang -d template_postgis plpgsql # Adding PLPGSQL language support.
psql -d template_postgis -f /usr/share/postgresql-8.3-postgis/lwpostgis.sql # Loading the PostGIS SQL routines
psql -d template_postgis -f /usr/share/postgresql-8.3-postgis/spatial_ref_sys.sql
psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;" # Enabling users to alter spatial tables.
psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
