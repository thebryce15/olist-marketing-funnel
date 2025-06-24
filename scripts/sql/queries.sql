-- Total leads by source
SELECT
  origin           AS source,
  COUNT(*)         AS total_leads
FROM public.olist_marketing_qualified_leads
GROUP BY origin
ORDER BY total_leads DESC;

-- Funnel Overview KPIs
WITH
  leads AS (
    SELECT
      origin                                   AS channel,
      COUNT(*)                                 AS total_leads
    FROM public.olist_marketing_qualified_leads
    GROUP BY 1
  ),
  conversions AS (
    SELECT
      ml.origin                                AS channel,
      COUNT(DISTINCT cd.mql_id)                AS total_conversions
    FROM public.olist_marketing_qualified_leads ml
    LEFT JOIN public.olist_closed_deals cd
      ON ml.mql_id = cd.mql_id
    GROUP BY 1
  ),
  revenue AS (
    SELECT
      ml.origin                                AS channel,
      SUM(oi.price + oi.freight_value)         AS total_revenue
    FROM public.olist_marketing_qualified_leads ml
    JOIN public.olist_closed_deals cd
      ON ml.mql_id = cd.mql_id
    JOIN public.olist_order_items oi
      ON oi.seller_id = cd.seller_id
    GROUP BY 1
  )
SELECT
  l.channel,
  l.total_leads,
  c.total_conversions,
  ROUND(c.total_conversions::numeric / NULLIF(l.total_leads,0), 4)    AS conversion_rate,
  ROUND(r.total_revenue::numeric   / NULLIF(l.total_leads,0),  2)    AS revenue_per_lead
FROM leads l
LEFT JOIN conversions c USING (channel)
LEFT JOIN revenue     r USING (channel)
ORDER BY l.total_leads DESC;

-- Lead volume vs Conversion Rate by Source
SELECT
  origin                                    AS channel,
  COUNT(*)                                  AS leads,
  ROUND(
    COUNT(cd.mql_id)::decimal
    / NULLIF(COUNT(*), 0)
    ,4
  )                                         AS conversion_rate
FROM public.olist_marketing_qualified_leads ml
LEFT JOIN public.olist_closed_deals cd
  ON ml.mql_id = cd.mql_id
GROUP BY 1
ORDER BY leads DESC;

-- Revenue Efficiency
SELECT
  ml.origin                                 AS channel,
  ROUND(
    SUM(oi.price + oi.freight_value)
    / NULLIF(COUNT(ml.mql_id),0)
    ,2
  )                                          AS revenue_per_lead,
  ROUND(
    SUM(oi.price + oi.freight_value)
    / NULLIF(COUNT(cd.mql_id),0)
    ,2
  )                                          AS avg_order_value
FROM public.olist_marketing_qualified_leads ml
LEFT JOIN public.olist_closed_deals cd
  ON ml.mql_id = cd.mql_id
LEFT JOIN public.olist_order_items oi
  ON oi.seller_id = cd.seller_id
GROUP BY 1
ORDER BY revenue_per_lead DESC;

--Trend Over Time
WITH
  monthly_leads AS (
    SELECT
      DATE_TRUNC('month', first_contact_date)::date AS month,
      origin                                      AS channel,
      COUNT(*)                                    AS total_leads
    FROM public.olist_marketing_qualified_leads
    GROUP BY 1,2
  ),

  monthly_conversions AS (
    SELECT
      DATE_TRUNC('month', ml.first_contact_date)::date AS month,
      ml.origin                                      AS channel,
      COUNT(DISTINCT cd.mql_id)                      AS total_conversions
    FROM public.olist_marketing_qualified_leads ml
    JOIN public.olist_closed_deals       cd
      ON ml.mql_id = cd.mql_id
    GROUP BY 1,2
  ),

  monthly_revenue AS (
    SELECT
      DATE_TRUNC('month', ml.first_contact_date)::date AS month,
      ml.origin                                      AS channel,
      SUM(oi.price + oi.freight_value)                AS total_revenue
    FROM public.olist_marketing_qualified_leads ml
    JOIN public.olist_closed_deals       cd
      ON ml.mql_id = cd.mql_id
    JOIN public.olist_order_items        oi
      ON cd.seller_id = oi.seller_id
    GROUP BY 1,2
  )

SELECT
  ml.month,
  ml.channel,
  ml.total_leads,
  COALESCE(mc.total_conversions, 0)  AS total_conversions,
  ROUND(
    COALESCE(mc.total_conversions,0)::numeric
    / NULLIF(ml.total_leads,0)
    ,4
  )                                   AS conversion_rate,
  ROUND(
    COALESCE(mr.total_revenue,0)::numeric
    / NULLIF(ml.total_leads,0)
    ,2
  )                                   AS revenue_per_lead
FROM monthly_leads ml
LEFT JOIN monthly_conversions  mc USING (month, channel)
LEFT JOIN monthly_revenue      mr USING (month, channel)
ORDER BY ml.month, ml.channel;



-- Funnel Drop Off Analysis
WITH funnel AS (
  SELECT
    ml.origin                                                  AS channel,
    COUNT(*)                                                    AS leads,
    COUNT(*) FILTER (WHERE ml.first_contact_date IS NOT NULL)   AS contacted,
    COUNT(cd.mql_id)                                            AS converted
  FROM public.olist_marketing_qualified_leads ml
  LEFT JOIN public.olist_closed_deals cd
    ON ml.mql_id = cd.mql_id
  GROUP BY 1
)
SELECT
  channel,
  ARRAY['leads','contacted','converted']                     AS stage,
  UNNEST(ARRAY[leads,contacted,converted])                   AS count
FROM funnel
ORDER BY channel;


