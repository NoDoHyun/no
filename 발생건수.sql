select 관서명, a.폭력 + a.살인 + a.`강간-강제추행` + a.강도 + a.절도 as 발생건수 from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as a
where 구분="발  생  건  수" group by 관서명
order by 발생건수
limit 1, 5
