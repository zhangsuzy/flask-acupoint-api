from flask import Flask, request, jsonify

app = Flask(__name__)

# 完整的五输穴数据库（名称 + 编号 + 取穴方法）
acupoint_data = {
    "肝": {
        "井穴": {"name": "大敦", "code": "LR1"},
        "荥穴": {"name": "行间", "code": "LR2"},
        "输穴": {"name": "太冲", "code": "LR3"},
        "经穴": {"name": "中封", "code": "LR4"},
        "合穴": {"name": "曲泉", "code": "LR8"}
    },
    "心": {
        "井穴": {"name": "少冲", "code": "HT9"},
        "荥穴": {"name": "少府", "code": "HT8"},
        "输穴": {"name": "神门", "code": "HT7"},
        "经穴": {"name": "灵道", "code": "HT4"},
        "合穴": {"name": "少海", "code": "HT3"}
    },
    "脾": {
        "井穴": {"name": "隐白", "code": "SP1"},
        "荥穴": {"name": "大都", "code": "SP2"},
        "输穴": {"name": "太白", "code": "SP3"},
        "经穴": {"name": "商丘", "code": "SP5"},
        "合穴": {"name": "阴陵泉", "code": "SP9"}
    },
    "肺": {
        "井穴": {"name": "少商", "code": "LU11"},
        "荥穴": {"name": "鱼际", "code": "LU10"},
        "输穴": {"name": "太渊", "code": "LU9"},
        "经穴": {"name": "经渠", "code": "LU8"},
        "合穴": {"name": "尺泽", "code": "LU5"}
    },
    "肾": {
        "井穴": {"name": "涌泉", "code": "KI1"},
        "荥穴": {"name": "然谷", "code": "KI2"},
        "输穴": {"name": "太溪", "code": "KI3"},
        "经穴": {"name": "复溜", "code": "KI7"},
        "合穴": {"name": "阴谷", "code": "KI10"}
    }
}

# 五行关系（用于选穴）
wuxing_relation = {
    "肝": {"母": "肾", "子": "心", "克": "金", "所不胜": "脾"},
    "心": {"母": "肝", "子": "脾", "克": "水", "所不胜": "肺"},
    "脾": {"母": "心", "子": "肺", "克": "木", "所不胜": "肾"},
    "肺": {"母": "脾", "子": "肾", "克": "火", "所不胜": "肝"},
    "肾": {"母": "肺", "子": "肝", "克": "土", "所不胜": "心"}
}


@app.route('/select_acupoint', methods=['GET'])
def select_acupoint():
    organ = request.args.get("organ")
    syndrome = request.args.get("syndrome")
    method = request.args.get("method")

    if organ not in wuxing_relation:
        return jsonify({"error": "无效的经络选择"})

    if method == "二针法":
        if syndrome == "虚证":
            return jsonify({
                "补母穴": acupoint_data[organ]["输穴"],
                "母经母穴": acupoint_data[wuxing_relation[organ]["母"]]["输穴"]
            })
        elif syndrome == "实证":
            return jsonify({
                "泻子穴": acupoint_data[organ]["荥穴"],
                "子经子穴": acupoint_data[wuxing_relation[organ]["子"]]["荥穴"]
            })

    if method == "四针法":
        if syndrome == "虚证":
            return jsonify({
                "补母穴": acupoint_data[wuxing_relation[organ]["母"]]["输穴"],
                "同经母穴": acupoint_data[organ]["输穴"],
                "泻所不胜穴": acupoint_data[wuxing_relation[organ]["所不胜"]]["输穴"],
                "泻本经所不胜穴": acupoint_data[organ]["经穴"]
            })
        elif syndrome == "实证":
            return jsonify({
                "泻子穴": acupoint_data[wuxing_relation[organ]["子"]]["荥穴"],
                "同经子穴": acupoint_data[organ]["荥穴"],
                "补所不胜穴": acupoint_data[wuxing_relation[organ]["所不胜"]]["输穴"],
                "本经所不胜穴": acupoint_data[organ]["经穴"]
            })

    return jsonify({"error": "无效的方法选择"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1999)
