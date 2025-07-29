
QUERIES = {

    'get_last_run_metadata': """
        with pipelines as (

            select * from etlcontrol{env}.pipelines.pipelines where pipeline_name = '{pipeline}'

        )
        , runs as (

            select * from etlcontrol{env}.pipelines.pipeline_runs

        )
        , states as (

            select * from etlcontrol{env}.pipelines.entity_states

        )
        , last_successful_run as (

            select 
                pipeline_id,
                max(run_id) as max_run_id
            from runs
            where was_successful = True
            group by 1

        )
        , run_data as (
            select
                runs.pipeline_id,
                runs.run_id,
                runs.run_start_at,
                runs.run_end_at
            from runs
            where exists (select 1 from last_successful_run where runs.run_id =  last_successful_run.max_run_id)
          
        )
        , joined as (

            select
                pipelines.pipeline_id,
                run_data.run_id,
                run_data.run_start_at,
                run_data.run_end_at,
                states.starting_watermark,
                states.high_watermark,
                states.starting_row_count,
                states.ending_row_count,
                states.extract_row_count,
                states.update_count,
                states.insert_count,
                states.delete_count,
                states.error_count
            from pipelines
            left join run_data
                on pipelines.pipeline_id = run_data.pipeline_id
            left join states
                on run_data.run_id = states.run_id

        )
        , final as (

            select
                run_id,
                run_start_at,
                run_end_at,
                pipeline_id,
                starting_watermark,
                high_watermark,
                starting_row_count,
                ending_row_count,
                extract_row_count,
                update_count,
                insert_count,
                delete_count,
                error_count
            from joined

        )
        select 
           *
        from final
        ;
        """,

    'insert_run_metadata': """
        insert into etlcontrol{env}.pipelines.pipeline_runs (
            pipeline_id,
            run_start_at,
            run_end_at,
            was_successful
        ) values (
            {pipeline_id},
            '{run_start_at}',
            '{run_end_at}',
            true
        )
        """,

    'get_run_id': """
        select
            max(run_id) as run_id
        from etlcontrol{env}.pipelines.pipeline_runs
        where pipeline_id = {pipeline_id}
        """,

    'insert_entity_metadata': """
        insert into etlcontrol{env}.pipelines.entity_states (
            pipeline_id,
            run_id,
            entity_name,
            starting_watermark,
            high_watermark,
            starting_row_count,
            ending_row_count,
            extract_row_count,
            update_count,
            insert_count,
            delete_count,
            error_count
        )
        select
            {pipeline_id},
            {run_id},
            '{entity_name}',
            parse_json('{starting_watermark}'),
            parse_json('{high_watermark}'),
            {starting_row_count},
            {ending_row_count},
            {extract_row_count},
            {update_count},
            {insert_count},
            {delete_count},
            {error_count}
        """,

    'new_pipeline': """
        insert into etlcontrol{env}.pipelines.pipelines (pipeline_name) 
        select '{pipeline}'
        where not exists (
            select 1 
            from etlcontrol{env}.pipelines.pipelines 
            where pipeline_name = '{pipeline}'
        );
        """,

    'get_pipeline_id': """
        select
            pipeline_id
        from etlcontrol{env}.pipelines.pipelines
        where pipeline_name = '{pipeline}' 
        """,

    'check_if_table_exists': """
        select
            to_boolean(count(1))
        from {db}.information_schema.tables
            where lower(table_schema) = '{schema_name}'
            and lower(table_name) = '{table_name}'
        ;
        """,

    'get_columns_and_data_type': """
        with columns_and_data_type as (
            select
                ordinal_position,
                column_name,
                data_type
            from {db}.information_schema.columns
            where lower(table_schema) = '{schema_name}'
            and lower(table_name) = '{table_name}'
            order by ordinal_position
        )
        select
            object_construct(
                'column_name', column_name,
                'data_type', data_type
            ) as column_properties
        from columns_and_data_type
        ;
    """

}
