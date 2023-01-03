select * from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as a
inner join `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as b
where 구분="발  생  건  수" group by 관서명