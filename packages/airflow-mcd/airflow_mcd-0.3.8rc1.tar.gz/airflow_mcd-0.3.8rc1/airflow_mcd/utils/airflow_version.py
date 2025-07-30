def airflow_major_version():
    try:
        import airflow
        return int(airflow.__version__.split('.')[0])
    except Exception:
        return 2  # fallback, assume 2 if unknown 