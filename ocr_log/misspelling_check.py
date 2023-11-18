from jamo import h2j, j2hcj
import re

case = ["ㅎㅕㄴㅈㅏㅇㅢㅌㅏㅂㅊㅡㅇㄹㅗㅂㅣ", "ㅇㅕㄴㄱㅡㅁㅅㅜㄹㅅㅏㅇㅈㅓㅁㄱㅏ", "ㅋㅘㄴㄷㅏㄴㅏㅁㅜㅂㅓㄹㅁㅗㄱㅌㅓ", "ㄱㅡㄴㅡㄹㅈㅣㄴㄷㅐㅇㅜㄹㅣㅁ", "ㅎㅗㅁㅜㄴㅋㅜㄹㄹㅜㅅㅡㅍㅖㄱㅣㅈㅏㅇ"]
region_in_boldaik = ["현자의 탑 1층 로비", "연금술 상점가", "콴다나무 벌목터", "그늘진 대우림", "호문쿨루스 폐기장"]

def split_jamo(str):
    return j2hcj(h2j(str))

def only_hangul(str):
    result = ''.join(re.findall('[ㄱ-ㅎㅏ-ㅣ]', str))
    return result

def levenshtein_distance(str1, str2):
    m = len(str1)
    n = len(str2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)

    return dp[m][n]

def distance_check(str1, str2, max_distance):
    distance = levenshtein_distance(str1, str2)

    if distance <= max_distance:
        return distance
    else:
        return 100

def make_spell(str):
    jamo = split_jamo(str)
    return only_hangul(jamo)

def word_check(str):
    spell = make_spell(str)
    nearest_case = 100
    matched_area = 0
    result = ""

    for i in range(len(case)):
        distance = distance_check(spell, case[i], 10)
        if distance != 100 and distance < nearest_case:
            nearest_case = distance
            matched_area = i

    if(nearest_case != 100):
        result = region_in_boldaik[matched_area]
    else:
        result = "no result"

    print(result)
    return result
