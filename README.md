# Example Streamlit in Snowpark Conatiner Services
This is a simple Streamlit that can be deployed in 
Snowpark Container Services. It queries the TPC-H 100 
data set and returns the top sales clerks. The Streamlit
provides date pickers to restrict the range of the sales
data and a slider to determine how many top clerks to display.
The data is presented in a table sorted by highest seller
to lowest.

# Setup
This example requires importing the `SNOWFLAKE_SAMPLE_DATA`
data share, and an account with Snowpark Container Services
enabled.

1. Follow the "Common Setup" [here](https://docs.snowflake.com/en/LIMITEDACCESS/snowpark-containers/tutorials/common-setup)
2. In a SQL Worksheet, execute `SHOW IMAGE REPOSITORIES` and look
   for the entry for `TUTORIAL_DB.DATA_SCHEMA.TUTORIAL_REPOSITORY`.
   Note the value for `repository_url`.
3. In the main directory of this repo, execute 
   `make configure`. Enter the URL of the repository that you
   noted in step 2 for the repository. Enter the name of the warehouse
   you set up in step 1 (if you followed the directions, it would be
   `tutorial_warehouse`).
4. Log into the Docker repository, build the Docker image, and push
   the image to the repository by running `make all`
   1. You can also run the steps individually. Log into the Docker 
      repository by running `make login` and entering your credentials.
   2. Make the Docker image by running `make build`.
   3. Push the image to the repository by running `make push_docker`
5. Create the service by executing the DDL. You can get this DDL
   by running `make ddl`:
```
CREATE SERVICE st_spcs
  IN COMPUTE POOL  tutorial_compute_pool
  FROM SPECIFICATION $$
spec:
  containers:
    - name: streamlit
      image: sfsenorthamerica-bmh-prod3.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/st_spcs
      env:
        SNOWFLAKE_WAREHOUSE: wh_xs
  endpoints:
    - name: streamlit
      port: 8080
      public: true  $$;
```
7. See that the service has started by executing `SHOW SERVICES IN COMPUTE POOL tutorial_compute_pool` and `SELECT system$get_service_status('st_spcs')`.
8. Find the public endpoint for the service by executing `SHOW ENDPOINTS IN SERVICE st_spcs`.
9. Grant permissions for folks to visit the Streamlit. You do this by granting 
   `USAGE` on the service: `GRANT USAGE ON SERVICE st_spcs TO ROLE some_role`, 
   where you specify the role in place of `some_role`.
10. Navigate to the endpoint and authenticate. Note, you must use a user whose
   default role is _not_ `ACCOUNTADMIN`, `SECURITYADMIN`, or `ORGADMIN`.
11. Enjoy!


## Local Testing
This Streamlit can be tested running locally. To do that, build the
image for your local machine with `make build_local`.

In order to run the Streamlit in the container, we need to set some 
environment variables in our terminal session before running the 
container. The variables to set are:
* `SNOWFLAKE_ACCOUNT` - the account locator for the Snowflake account
* `SNOWFLAKE_USER` - the Snowflake username to use
* `SNOWFLAKE_PASSWORD` - the password for the Snowflake user
* `SNOWFLAKE_WAREHOUSE` - the warehouse to use
* `SNOWFLAKE_DATABASE` - the database to set as the current database (does not really matter that much what this is set to)
* `SNOWFLAKE_SCHEMA` - the schema in the database to set as the current schema (does not really matter that much what this is set to)

Once those have been set, run the Streamlit container with `make run`. Navigate
to `http://localhost:8080`.