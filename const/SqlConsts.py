# stock_info表
truncate_stock = 'truncate table stock_info'
stock_insert_sql = 'INSERT INTO stock_info(ts_code, symbol, name,area, industry,list_date) VALUES(%s, %s, %s, %s, %s, %s)'
select_by_symbol = 'select *from stock_info where symbol=%s'
select_by_name = 'select *from stock_info where name=%s'

# xq_data表
del_stock_history_by_date = 'delete from xq_data where date=%s'
stock_history_insert_sql = 'INSERT INTO xq_data(symbol,name,current,percent,amplitude,amount,volume_ratio,current_year_percent,turnover_rate,market_capital,date,create_time) VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s,%s)'
stock_history_select = 'select date,symbol,name,percent,current_year_percent,amount,turnover_rate,market_capital from xq_data where date = %s  and percent>= %s and current_year_percent  BETWEEN %s and  %s  ORDER BY percent DESC'
