select a.구분, a.세대수, a.`인구(명)`, a.`공무원(명)`, a.`면적(제곱킬로미터)`, (`인구(명)`/`공무원(명)`)  as "공무원 1인당 인구(명)", round(`인구(명)`/`면적(제곱킬로미터)`) as "인구밀도(명/제곱킬로미터)", b.폭력 + b.살인 + b.`강간-강제추행` + b.강도 + b.절도 as 범죄발생건수
from `crime`.`광주광역시_자치구별 현황_20210731` as a
inner join `crime`.`경찰청 광주광역시경찰청_자치구별 5대 범죄 현황_20211231` as b
on mid(a.구분, 7, 1) = mid(b.관서명, 3, 1)
group by 관서명
order by 범죄발생건수
limit 1, 5

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