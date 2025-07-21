def generate_mysql_query(
    platforms, auction_type, bsns_vrtcl_name, buyer_segment,
    enthusiasts_yn, new_buyer_yn, price_bucket, site, traffic_source, session_date_range,
    engmnt_lv1_desc=None, expertise_desc=None, b2c_c2c=None, avip_cvip=None, msku_ind=None, fcsd_vrtcl_name=None, itm_condition=None,
    viewport_width=None, source_page_name=None
):
    filters = []

    def build_condition(field, value):
        if value == "(All)" or not value:
            return None
        return f"{field} = '{value}'"

    filters.append(build_condition("auction_type", auction_type))
    filters.append(build_condition("business_vertical", bsns_vrtcl_name))
    filters.append(build_condition("buyer_segment", buyer_segment))
    filters.append(build_condition("enthusiasts_flag", enthusiasts_yn))
    filters.append(build_condition("new_buyer_flag", new_buyer_yn))
    filters.append(build_condition("price_bucket", price_bucket))
    filters.append(build_condition("site", site))
    filters.append(build_condition("traffic_source", traffic_source))

    # Add new variables to filter logic
    filters.append(build_condition("engagement_lv1_desc", engmnt_lv1_desc))
    filters.append(build_condition("expertise_desc", expertise_desc))
    filters.append(build_condition("b2c_c2c", b2c_c2c))
    filters.append(build_condition("avip_cvip", avip_cvip))
    filters.append(build_condition("msku_indicator", msku_ind))
    filters.append(build_condition("fcsd_vertical_name", fcsd_vrtcl_name))
    filters.append(build_condition("item_condition", itm_condition))
    filters.append(build_condition("viewport_width", viewport_width))
    filters.append(build_condition("source_page_name", source_page_name))

    if platforms:
        platform_condition = "platform IN (" + ",".join(f"'{p}'" for p in platforms) + ")"
        filters.append(platform_condition)

    start, end = session_date_range
    filters.append(f"session_start_date BETWEEN '{start}' AND '{end}'")

    where_clause = " AND ".join([f for f in filters if f])
    query = f"""
        SELECT *
        FROM vi_module_metrics
        WHERE {where_clause}
    """
    return query.strip()