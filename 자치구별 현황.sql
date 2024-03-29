select c.경찰서, round(a.`인구(명)`/10000) as "인구(만명)", b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도 as 범죄발생건수, round((b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / a.`인구(명)` * 10000) as "인구 1만명당 범죄 건수", (b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) / `면적(제곱킬로미터)` as "범죄 건수/면적(km²)", c.검거건수, c.검거건수/(b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도) * 100 as "검거율(%)", round(sum(d.카메라대수)/18) as 카메라대수, a.`인구(명)`/(sum(d.카메라대수)/18) as "카메라 1대당 인구수" from `crime`.`광주광역시_자치구별 현황_20210731` as a inner join `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as b inner join `crime`.`category` as c inner join `crime`.`광주광역시_cctv_20220429` as d on mid(d.소재지지번주소, 7, 1) = mid(c.경찰서, 3, 1) on mid(c.경찰서, 3, 1) = mid(b.관서명, 3, 1) on mid(a.구분, 7, 1) = mid(b.관서명, 3, 1) group by 관서명 order by 범죄발생건수 limit 1, 5

-- select 관서명, a.폭력 + a.살인 + a.`강간-강제추행` + a.강도 + a.절도 as 발생건수 from `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as a
-- where 구분="발  생  건  수" group by 관서명
-- order by 발생건수
-- limit 1, 5


-- b.관서명, b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도 as 발생건수
-- select 구분, 세대수 from `crime`.`광주광역시_자치구별 현황_20210731`
-- select 세대수 from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 동구"
-- select 세대수 from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 서구"
-- select 세대수 from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 남구"
-- select 세대수 from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 북구"
-- select 세대수 from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 광산구"

-- select 구분, `면적(제곱킬로미터)` from `crime`.`광주광역시_자치구별 현황_20210731`
-- select `면적(제곱킬로미터)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 동구"
-- select `면적(제곱킬로미터)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 서구"
-- select `면적(제곱킬로미터)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 남구"
-- select `면적(제곱킬로미터)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 북구"
-- select `면적(제곱킬로미터)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 광산구"

-- select 구분, `공무원(명)` from `crime`.`광주광역시_자치구별 현황_20210731`
-- select `공무원(명)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 동구"
-- select `공무원(명)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 서구"
-- select `공무원(명)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 남구"
-- select `공무원(명)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 북구"
-- select `공무원(명)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 광산구"

-- select 구분, `인구(명)` from `crime`.`광주광역시_자치구별 현황_20210731`
-- select `인구(명)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 동구"
-- select `인구(명)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 서구"
-- select `인구(명)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 남구"
-- select `인구(명)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 북구"
-- select `인구(명)` from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 광산구"

-- select 구분, round(`인구(명)`/`공무원(명)`)  as "공무원 1인당 인구(명)" from `crime`.`광주광역시_자치구별 현황_20210731`
-- select round(`인구(명)`/`공무원(명)`)  as "공무원 1인당 인구(명)" from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 동구"
-- select round(`인구(명)`/`공무원(명)`)  as "공무원 1인당 인구(명)" from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 서구"
-- select round(`인구(명)`/`공무원(명)`)  as "공무원 1인당 인구(명)" from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 남구"
-- select round(`인구(명)`/`공무원(명)`)  as "공무원 1인당 인구(명)" from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 북구"
-- select round(`인구(명)`/`공무원(명)`)  as "공무원 1인당 인구(명)" from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 광산구"

-- select 구분, round(`인구(명)`/`면적(제곱킬로미터)`)  as "인구밀도(명/제곱킬로미터)" from `crime`.`광주광역시_자치구별 현황_20210731`
-- select round(`인구(명)`/`면적(제곱킬로미터)`)  as "인구밀도(명/제곱킬로미터)" from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 동구"
-- select round(`인구(명)`/`면적(제곱킬로미터)`)  as "인구밀도(명/제곱킬로미터)" from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 서구"
-- select round(`인구(명)`/`면적(제곱킬로미터)`)  as "인구밀도(명/제곱킬로미터)" from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 남구"
-- select round(`인구(명)`/`면적(제곱킬로미터)`)  as "인구밀도(명/제곱킬로미터)" from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 북구"
-- select round(`인구(명)`/`면적(제곱킬로미터)`)  as "인구밀도(명/제곱킬로미터)" from `crime`.`광주광역시_자치구별 현황_20210731` where 구분="광주광역시 광산구"