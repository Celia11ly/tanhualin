#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory, make_response
import json
import os
import random
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# 读取JSON数据
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'output.json')
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 处理数据，构建模块分层结构
modules = {}
current_level1 = None
current_level2 = None

for item in data:
    level1 = item.get('一级模块')
    level2 = item.get('二级模块')
    content = item.get('模块内容')
    
    if level1:
        current_level1 = level1
        if current_level1 not in modules:
            modules[current_level1] = {}
        current_level2 = None
    
    if level2:
        current_level2 = level2
        if current_level2 not in modules[current_level1]:
            modules[current_level1][current_level2] = []
    
    if content:
        if current_level2:
            modules[current_level1][current_level2].append(content)
        elif current_level1:
            # 设备管理模块不添加未分类内容
            if current_level1 != '设备管理':
                if '未分类' not in modules[current_level1]:
                    modules[current_level1]['未分类'] = []
                modules[current_level1]['未分类'].append(content)

@app.route('/')
def index():
    return render_template('index.html', modules=modules)

@app.route('/api/modules')
def get_modules():
    return jsonify(modules)

@app.route('/module/')
def module_list():
    return redirect(url_for('index'))

@app.route('/module/<level1_name>')
def module_page(level1_name):
    # 处理URL编码的特殊字符
    level1_name = level1_name.replace('-', ' ')

    # 特殊处理NGD智能客服对话模块
    if level1_name == 'NGD智能客服对话模块':
        # 为当前一级模块生成样本数据
        sample_data = generate_sample_data(level1_name, '')

        # 获取当前一级模块下的所有二级模块
        level2_modules = list(modules[level1_name].keys())
        print(f"NGD智能客服对话模块下的二级模块数量: {len(level2_modules)}")
        print(f"二级模块列表: {level2_modules}")

        # 渲染专用的模板或传递特殊标志
        return render_template('module.html', level1_name=level1_name, sample_data=sample_data, modules=modules, level2_modules=level2_modules, get_icon=get_icon, is_ngd_module=True)

    # 特殊处理自定义开发、会话详情和设备管理模块
    if level1_name == '自定义开发':
        return render_template('custom_dev.html', level1_name=level1_name)
    elif level1_name == '会话详情':
        return render_template('session_detail.html', level1_name=level1_name)
    elif level1_name == '设备管理':
        return render_template('device_management.html', level1_name=level1_name)

    # 检查是否是一级模块
    if level1_name in modules:
        # 为当前一级模块生成样本数据
        sample_data = generate_sample_data(level1_name, '')

        # 获取当前一级模块下的所有二级模块
        level2_modules = list(modules[level1_name].keys())

        return render_template('module.html', level1_name=level1_name, sample_data=sample_data, modules=modules, level2_modules=level2_modules, get_icon=get_icon)
    
    # 检查是否是某个一级模块下的二级模块
    for level1 in modules:
        if level1_name in modules[level1]:
            return redirect(url_for('feature_page', level1_name=level1, level2_name=level1_name))
    
    return render_template('error.html', message='模块不存在'), 404

@app.route('/module/<level1_name>/<level2_name>')
def feature_page(level1_name, level2_name):
    # 处理URL编码的特殊字符
    level1_name = level1_name.replace('-', ' ')
    level2_name = level2_name.replace('-', ' ')
    if level1_name not in modules or level2_name not in modules[level1_name]:
        return render_template('error.html', message='功能不存在'), 404
    # 为功能项生成一些示例数据
    sample_data = generate_sample_data(level1_name, level2_name)
    
    # 特殊处理实体模块
    if level1_name == 'NGD智能客服对话模块' and level2_name == '实体':
        # 创建模拟的current_user对象
        class MockUser:
            def __init__(self):
                self.initials = 'AD'
                self.username = 'admin'
        current_user = MockUser()
        return render_template('entity.html', level1_name=level1_name, level2_name=level2_name, entity_data=sample_data, current_user=current_user)
    # 特殊处理意图模块
    elif level1_name == 'NGD智能客服对话模块' and level2_name == '意图':
        # 创建模拟的current_user对象
        class MockUser:
            def __init__(self):
                self.initials = 'AD'
                self.username = 'admin'
        current_user = MockUser()
        return render_template('intent.html', level1_name=level1_name, level2_name=level2_name, intent_data=sample_data, current_user=current_user)
    # 特殊处理Bot管理模块
    elif level1_name == 'NGD智能客服对话模块' and level2_name == 'Bot 管理':
        return render_template('bot_management.html', level1_name=level1_name, level2_name=level2_name)
    # 特殊处理意图模型管理模块
    elif level1_name == 'NGD智能客服对话模块' and level2_name == '意图模型管理':
        return render_template('intent_model_management.html', level1_name=level1_name, level2_name=level2_name)
    # 特殊处理FAQ问答模块
    elif level1_name == 'NGD智能客服对话模块' and level2_name == 'FAQ 问答':
        # 创建模拟的current_user对象
        class MockUser:
            def __init__(self):
                self.initials = 'AD'
                self.username = 'admin'
        current_user = MockUser()
        # 从sample_data中提取FAQ数据和分类数据
        faq_data = sample_data
        # 生成分类数据（从FAQ数据中提取唯一分类）
        categories = []
        if faq_data:
            category_set = set()
            for faq in faq_data:
                if faq['category'] not in category_set:
                    category_set.add(faq['category'])
                    # 模拟子分类
                    sub_categories = []
                    sub_category_set = set()
                    for sub_faq in faq_data:
                        if sub_faq['category'] == faq['category']:
                            sub_cat = sub_faq['sub_category'].split('-')[0]
                            if sub_cat not in sub_category_set:
                                sub_category_set.add(sub_cat)
                                sub_categories.append({
                                    'id': f'SUB_{len(sub_categories) + 1:03d}',
                                    'name': sub_cat
                                })
                    categories.append({
                        'id': f'CAT_{len(categories) + 1:03d}',
                        'name': faq['category'],
                        'children': sub_categories
                    })
        # 分页处理
        page = request.args.get('page', 1, type=int)
        per_page = 10
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_faqs = faq_data[start_index:end_index]
        total_count = len(faq_data)
        total_pages = (total_count + per_page - 1) // per_page
        # 确定要显示的页码范围
        max_pages_to_show = 5
        if total_pages <= max_pages_to_show:
            pages_to_show = list(range(1, total_pages + 1))
        else:
            half = max_pages_to_show // 2
            if page - half <= 1:
                pages_to_show = list(range(1, max_pages_to_show + 1))
            elif page + half >= total_pages:
                pages_to_show = list(range(total_pages - max_pages_to_show + 1, total_pages + 1))
            else:
                pages_to_show = list(range(page - half, page + half + 1))
        return render_template('faq.html',
                              level1_id=level1_name,
                              level1_name=level1_name,
                              category_data=categories,
                              faq_data=paginated_faqs,
                              current_category_id=categories[0]['id'] if categories else None,
                              current_sub_category_id=None,
                              start_index=start_index + 1,
                              end_index=min(end_index, total_count),
                              total_count=total_count,
                              current_page=page,
                              total_pages=total_pages,
                              pages_to_show=pages_to_show,
                              current_user=current_user)
    # 特殊处理机器人闲聊模块
    elif level1_name == 'NGD智能客服对话模块' and level2_name == '机器人闲聊':
        # 创建模拟的current_user对象
        class MockUser:
            def __init__(self):
                self.initials = 'AD'
                self.username = 'admin'
        current_user = MockUser()
        return render_template('chat.html',
                              level1_name=level1_name,
                              level2_name=level2_name,
                              sample_data=sample_data,
                              current_user=current_user)
    # 特殊处理接口指令模块
    elif level1_name == 'NGD智能客服对话模块' and level2_name == '接口指令':
        # 创建模拟的current_user对象
        class MockUser:
            def __init__(self):
                self.initials = 'AD'
                self.username = 'admin'
        current_user = MockUser()
        return render_template('command.html',
                              level1_name=level1_name,
                              level2_name=level2_name,
                              sample_data=sample_data,
                              current_user=current_user)
    
    return render_template('feature.html', level1_name=level1_name, level2_name=level2_name, sample_data=sample_data)

# 为技能库模块提供数据的API
@app.route('/api/skills')
def get_skills():
    level1_name = '技能管理'
    level2_name = '技能库'
    if level1_name not in modules or level2_name not in modules[level1_name]:
        return jsonify({'error': '技能库模块不存在'}), 404
    # 生成技能数据
    skills_data = generate_sample_data(level1_name, level2_name)
    return jsonify(skills_data)

# 为模块分配图标
def get_icon(module_name):
    icons = {
        '用户管理': 'users',
        '角色权限': 'key',
        '数据统计': 'pie-chart',
        '系统设置': 'cog',
        '技能配置': 'wrench',
        '技能训练': 'graduation-cap',
        '代码编辑': 'code',
        '接口管理': 'plug',
        '接口指令': 'terminal',
        '会话记录': 'history',
        '会话分析': 'bar-chart',
        '运营数据': 'line-chart',
        '活动管理': 'calendar',
        '智能问答': 'comment-o',
        '对话流程': 'sitemap',
        '技能库': 'book',
        '实体': 'database',
        '意图': 'lightbulb-o',
        'FAQ 问答': 'question-circle-o',
        '机器人闲聊': 'comment-dots',
        # 默认图标
        'default': 'folder'
    }
    
    for key in icons:
        if key in module_name:
            return icons[key]
    return icons['default']

def generate_sample_data(level1_name, level2_name):
    """生成示例数据"""
    data = []
    if level1_name == '技能管理' and level2_name == '技能库':
        # 技能库数据
        industries = ['tech', 'finance', 'healthcare', 'education', 'retail']
        industry_names = {'tech': '科技', 'finance': '金融', 'healthcare': '医疗健康', 'education': '教育', 'retail': '零售'}
        levels = ['初级', '中级', '高级', '专家']
        skill_names = [
            'Python编程', '数据分析', '机器学习', '深度学习', '自然语言处理',
            '计算机视觉', '前端开发', '后端开发', '移动应用开发', '云计算',
            '大数据处理', '区块链开发', '网络安全', 'DevOps', 'UI/UX设计',
            '产品管理', '项目管理', '市场营销', '销售技巧', '客户服务'
        ]
        for i in range(1, 21):
            industry = random.choice(industries)
            data.append({
                'id': f'SK{i:03d}',
                'name': random.choice(skill_names),
                'description': f'这是一项关于{random.choice(skill_names)}的{random.choice(levels)}技能，适用于{industry_names[industry]}行业。',
                'industry': industry_names[industry],
                'industry_code': industry,
                'level': random.choice(levels),
                'created_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                'is_template': random.choice([True, False])
            })
    elif level1_name == 'NGD智能客服对话模块':
        # 为NGD智能客服对话模块生成实际的子模块数据
        if level2_name == '':
            # 一级模块页面，返回二级模块列表
            return list(modules[level1_name].keys())
        elif level2_name == '会话流程':
            # 为会话流程模块生成示例数据
            data = []
            for i in range(1, 11):
                status = random.choice(['active', 'completed', 'draft', 'template'])
                data.append({
                    'id': f'SS{i:03d}',
                    'name': f'会话流程{i}',
                    'created_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                    'updated_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                    'version': f'{random.randint(1,3)}.{random.randint(0,9)}',
                    'status': status
                })
        elif level2_name == '实体':
            # 为实体模块生成示例数据
            data = []
            entity_types = ['user', 'system', 'rule', 'composite']
            entity_status = ['active', 'inactive', 'draft']
            entity_names = [
                '客户信息', '产品分类', '订单状态', '支付方式', '配送地址',
                '优惠券类型', '会员等级', '商品属性', '活动标签', '用户行为'
            ]
            for i in range(1, 11):
                entity_type = random.choice(entity_types)
                status = random.choice(entity_status)
                data.append({
                    'id': f'EN{i:03d}',
                    'name': random.choice(entity_names),
                    'type': entity_type,
                    'status': status,
                    'created_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                    'updated_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
                })
        elif level2_name == '意图':
            # 为意图模块生成示例数据
            data = []
            intent_status = ['active', 'inactive', 'draft']
            intent_types = ['normal', 'system', 'fallback']
            intent_names = [
                '咨询产品', '投诉建议', '预约服务', '售后服务', '退款申请',
                '账户问题', '配送查询', '订单修改', '优惠券使用', '会员政策'
            ]
            for i in range(1, 11):
                data.append({
                    'id': f'IT{i:03d}',
                    'name': random.choice(intent_names),
                    'type': random.choice(intent_types),
                    'description': f'这是一个{random.choice(intent_types)}类型的意图，用于处理用户关于{random.choice(intent_names)}的请求。',
                    'status': random.choice(intent_status),
                    'sample_count': random.randint(5, 30),
                    'created_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
                })
        elif level2_name == 'FAQ 问答':
            # 为FAQ问答模块生成示例数据
            data = []
            faq_status = ['active', 'inactive', 'draft']
            faq_categories = ['产品咨询', '售后服务', '配送政策', '支付方式', '会员政策', '优惠券使用', '退款说明']
            faq_templates = [True, False]
            for i in range(1, 11):
                # 模拟多级目录
                category = random.choice(faq_categories)
                sub_category = f'{category}-{random.randint(1, 3)}'
                
                # 模拟关联问题
                related_questions = [f'相关问题{i+1}' for i in range(random.randint(1, 3))]
                
                # 模拟多渠道答案
                channels = {
                    'app': f'APP渠道答案 {i}',
                    'web': f'网页渠道答案 {i}',
                    'wechat': f'微信渠道答案 {i}'
                }
                
                # 模拟相似问题
                similar_questions = [f'相似问题{i+1}' for i in range(random.randint(1, 4))]
                
                data.append({
                    'id': f'FQ{i:03d}',
                    'question': f'FAQ问题{i}',
                    'answer': f'这是FAQ问题{i}的标准答案。',
                    'category': category,
                    'sub_category': sub_category,
                    'related_questions': related_questions,
                    'channels': channels,
                    'similar_questions': similar_questions,
                    'is_template': random.choice(faq_templates),
                    'status': random.choice(faq_status),
                    'created_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
                })
            return data
        elif level2_name == '机器人闲聊':
            # 为机器人闲聊模块生成示例数据
            data = {
                'chats': [],
                'personalities': []
            }
            # 生成闲聊数据
            chat_status = ['active', 'inactive', 'draft']
            chat_types = ['greeting', 'farewell', 'small_talk', 'joke', 'weather', 'recommendation']
            for i in range(1, 11):
                data['chats'].append({
                    'id': f'CT{i:03d}',
                    'question': f'闲聊问题{i}',
                    'answer': f'这是闲聊问题{i}的回答。',
                    'type': random.choice(chat_types),
                    'status': random.choice(chat_status),
                    'created_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
                })
            # 生成人设数据
            personality_status = ['active', 'inactive']
            personality_names = ['亲切型', '专业型', '幽默型', '可爱型', '成熟型']
            for i in range(1, 6):
                data['personalities'].append({
                    'id': f'PS{i:03d}',
                    'name': random.choice(personality_names),
                    'description': f'这是一个{random.choice(personality_names)}的人设。',
                    'status': random.choice(personality_status),
                    'created_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
                })
            return data
        elif level2_name == '接口指令':
            # 为接口指令模块生成示例数据
            data = []
            command_status = ['active', 'inactive', 'draft']
            command_types = ['system', 'custom', 'webhook']
            command_names = [
                '获取用户信息', '更新订单状态', '发送通知', '查询库存', '创建用户',
                '删除记录', '同步数据', '调用API', '执行脚本', '推送消息'
            ]
            for i in range(1, 11):
                data.append({
                    'id': f'CD{i:03d}',
                    'name': random.choice(command_names),
                    'type': random.choice(command_types),
                    'description': f'这是一个{random.choice(command_types)}类型的接口指令，用于{random.choice(command_names)}。',
                    'status': random.choice(command_status),
                    'created_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
                })
            return data
        # 其他模块数据生成逻辑
        data = []
        intent_status = ['active', 'inactive', 'draft']
        intent_names = [
            '查询订单', '取消订单', '投诉反馈', '商品咨询', '退款申请',
            '物流查询', '账户注册', '密码重置', '优惠券领取', '活动参与'
        ]
        for i in range(1, 11):
            status = random.choice(intent_status)
            data.append({
                'id': f'IT{i:03d}',
                'name': random.choice(intent_names),
                'description': f'这是一个{random.choice(["高频", "中频", "低频"])}{"的"}{random.choice(intent_names)}意图。',
                'status': status,
                'sample_count': random.randint(5, 50),
                'created_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
                'updated_at': f'2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
            })
        return data
    return data

@app.route('/test')
def test_page():
    return render_template('test.html')

@app.route('/static-test')
def static_test():
    return send_from_directory('.', 'static_test.html')

@app.route('/faq')
def faq_page():
    # 测试FAQ问答模块
    data = generate_sample_data('NGD智能客服对话模块', 'FAQ 问答')
    return render_template('faq.html', data=data)

# 机器人闲聊导入Excel
@app.route('/api/chat/import', methods=['POST'])
def import_chat():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件被上传'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        try:
            # 读取Excel文件
            df = pd.read_excel(file)
            # 转换为JSON
            chat_data = df.to_dict(orient='records')
            # 在实际应用中，这里会将数据保存到数据库
            return jsonify({'success': True, 'message': '导入成功', 'data': chat_data}), 200
        except Exception as e:
            return jsonify({'error': f'导入失败: {str(e)}'}), 500
    else:
        return jsonify({'error': '请上传Excel文件(.xlsx或.xls)'}), 400

# 机器人闲聊导出Excel
@app.route('/api/chat/export', methods=['GET'])
def export_chat():
    try:
        # 获取闲聊数据
        chat_data = generate_sample_data('NGD智能客服对话模块', '机器人闲聊')['chats']
        # 转换为DataFrame
        df = pd.DataFrame(chat_data)
        # 创建Excel文件
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='闲聊数据')
        output.seek(0)
        # 创建响应
        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=chat_data.xlsx'
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return response
    except Exception as e:
        return jsonify({'error': f'导出失败: {str(e)}'}), 500

import os

if __name__ == '__main__':
    # 确保templates文件夹存在
    if not os.path.exists('templates'):
        os.makedirs('templates')
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)