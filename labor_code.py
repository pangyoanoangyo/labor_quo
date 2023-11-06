labor_kr = ["통신내선공", "통신설비공", "통신외선공", "통신케이블공", "무선안테나공", "보통인부",
            "특별인부", "광케이블 설치사", "H/W시험사", "S/W시험사", "통신관련기사", "통신관련산업기사", "통신관련기능사"]
labor_en = ["tele_naesun", "tele_sulbi", "tele_owibu", "tele_cable", "antenna",
            "normal_person", "special_person", "fiber_cable", "hw", "sw", "tele_gisa", "tele_sanup", "tele_gi",]
salary = [251790, 280506, 363102, 389536, 319190, 157068,
          197450, 409726, 354947, 401195, 292454, 284281, 234222,]


# 딕셔너리로 정리해보자
labor_dict = {}
for i in labor_kr:
    for j in salary:
        labor_dict[i] = j


labor_detail = {
    'dome': [0, 0.18, 0, 0, 0, 0, 0.18, 0, 0, 0, 0, 0, 0],
    'bullet': [0, 0.24, 0, 0, 0, 0, 0.24, 0, 0, 0, 0, 0, 0],
    'MODULAR': [0, 0.24, 0, 0, 0, 0, 0.24, 0, 0, 0, 0, 0, 0],
    'ptz': [0, 0.32, 0, 0, 0, 0, 0.32, 0, 0, 0, 0, 0, 0],
    'bracket_normal': [5, 0, 0.23, 0, 0, 0, 0, 0.23, 0, 0, 0, 0, 0, 0],
    'bracket_ceiling': [6, 0, 0.31, 0, 0, 0, 0, 0.31, 0, 0, 0, 0, 0, 0],
    'ptz_driver': [0.53, 0, 0, 0, 0, 0.53, 0, 0, 0, 0, 0, 0, 0],
    'lift': [0, 0.34, 0, 0, 0, 0, 0, 0, 0, 0, 0.34, 0, 0],
    'lift_control': [0, 0.34, 0, 0, 0, 0, 0, 0, 0, 0, 0.34, 0, 0],
    'nvr': [0, 0.18, 0, 0, 0, 0, 0, 0, 0, 0, 0.18, 0, 0],
    'dvr': [0, 0.18, 0, 0, 0, 0, 0, 0, 0, 0, 0.18, 0, 0],
    'OTHERS': [11, 0, 0.18, 0, 0, 0, 0.53, 0, 0, 0, 0, 0.18, 0, 0],
    'ENC/DEC': [0, 0.2, 0, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0],
    '송수신기': [0, 0.2, 0, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0],
    'decoder': [0, 0.2, 0, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0],
    'cam_3': [0, 0.18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.06, 0],
    'cam_12': [0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.08, 0],
    'inform_pannel': [16, 0, 0.37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.37, 0],
    'cms': [0, 0.84, 0, 1.26, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'out_car': [0.21, 0.21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'cam_3': [0, 0.18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.06, 0],
    'cam_12': [0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.08, 0],
    'inform_pannel': [0, 0.37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.37, 0],
    'dv': [0, 0.84, 0, 1.26, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'cms': [0, 0.84, 0, 1.26, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'out_car': [0.21, 0.21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'hub_install': [0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, 0, 0],
    'card_install': [0, 0.18, 0, 0, 0, 0, 0, 0, 0, 0, 0.18, 0, 0],
    'control': [0, 0, 0, 0, 0, 0, 0, 0, 0.42, 0.42, 0, 0, 0],
    'NET SWITCH': [0, 0, 0, 0, 0, 0, 0, 0, 0.4, 0.4, 0, 0, 0],
}


# print(f"labor_dict : {labor_dict}")
# print(f"labor_detail : {labor_detail}")


def labor_calc(p):
    # print(f"p : {p}")
    for k, v in labor_detail.items():
        k = k.upper()
        # print(f"i : {k}")
        if k == p:  # 예를 들어 p가 dome이면
            # print("디테일에 있습니다")
            p = v  # p에 v를 넣는다.
    a = []
    b = 0
    result = 0
    # print("p", len(p), p)
    for i in range(0, len(p)):
        if isinstance(p[i], (int, float)) and isinstance(salary[i], (int, float)):
            b = p[i] * salary[i]
            a.append(b)
        else:
            print(
                f"Error: Non-numeric value found at index {i}, p[i]: {p[i]}, salary[i]: {salary[i]}")
            # 여기서 적절한 에러 처리를 해야 합니다.

    result = sum(a)  # a의 합을 result에 넣는다.
    print(type(result), result)

    # print(f"labor_calc 함수가 정상작동합니다")

    return result


# print(labor_calc('dome'))
