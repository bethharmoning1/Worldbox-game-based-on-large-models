import re
import flet as ft
import flet_fastapi
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("/data/gxq/Qwen/Qwen_int4", trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    "/data/gxq/Qwen/Qwen_int4",
    device_map="auto",
    trust_remote_code=True
).eval()

history_init = [('你是一个语言学家，专门研究词语之间的联系。现在进行一个合成小游戏，给你两个物体名词，以“甲+乙”的形式，请你给出它们合成之后最可能的词语（词性必须为名词），并给该词语一个1星至5星的评级，并说明给出该评级的理由。例如：火+水=灰烬（1星）-常见的物质。为给定问题生成富有逻辑且尽可能短的答案（不超过4个字，越短越好）。不要简单的将两个词叠加起来。不要重复文本。不要生成英文。如果不同的结果引用具有相同名称的不同实体，请为每个实体编写单独的答案。请生成10个样例。',
 '1. 蜂+蜜=蜂蜜（5星）-最常见的食物。\n2. 雨+伞=雨伞（5星）-日常用品。\n3. 书+包=书包（5星）-学习用品。\n4. 水+杯=水杯（5星）-日常生活必需品。\n5. 火+柴=火柴（5星）-生活必备工具。\n6. 墙+壁挂画=壁挂（5星）-家居装饰品。\n7. 手+机=手机（5星）-现代通讯工具。\n8. 笔+纸=笔记（5星）-常用的学习和工作工具。\n9. 牛+奶=牛奶（5星）-营养丰富的饮品。\n10. 猪+肉=猪肉（5星）-常见的肉类食品。')]
global cnt
global prompt
prompt = ''
cnt = 0


def choose_star_color(num):
    if num == '1':
        return ft.colors.GREY
    elif num == '2':
        return ft.colors.GREEN
    elif num == '3':
        return ft.colors.BLUE
    elif num == '4':
        return ft.colors.PURPLE
    elif num == '5':
        return ft.colors.ORANGE
    else:
        return ft.colors.BLACK

def main(page: ft.Page):
    def button_clicked(param):
        global cnt
        global prompt
        if cnt == 0:
            cnt = cnt + 1
            prompt = param
            Intro_text.value = param + '+'
            Info_text.value = ''
            Info_text.spans = []
            page.update()
        else:
            cnt = 0
            prompt = prompt + '+' + param
            print('Begin: '+prompt)
            Intro_text.value = Intro_text.value + param + '='
            Side_tab.controls.append(ft.ProgressRing())
            Side_tab.controls.append(ft.Text("计算中……"))
            page.update()
            response, history = model.chat(tokenizer, prompt, history=history_init)
            pattern1 = r'.*=(.*)（(.*)星）-(.*)'
            pattern2 = r'(.*)（(.*)星）-(.*)'
            print(response)
            try:
                splitted = re.search(pattern1,response)
                assert splitted is not None
            except:
                splitted = re.search(pattern2,response)
            obj = splitted.group(1)
            Intro_text.value = Intro_text.value + obj
            star = splitted.group(2)
            intro = splitted.group(3)
            
            Info_text.spans = [
                ft.TextSpan(star + '星' + '\t-\t',ft.TextStyle(weight=ft.FontWeight.BOLD,color=choose_star_color(star))),
                ft.TextSpan(intro,ft.TextStyle(weight=ft.FontWeight.BOLD,color=ft.colors.GREY))
            ]
            Side_tab.controls.pop()
            Side_tab.controls.pop()
            images.controls.append(ft.ElevatedButton(
                            adaptive=True, 
                            bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
                            content=ft.Row(
                                [
                                    ft.Text(obj,size=20, color="black", italic=True),
                                ],
                                tight=True,
                                ),
                                 on_click=lambda e: button_clicked(obj))
                    )
            page.update()
    images = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )
    images.controls.append(
            ft.ElevatedButton(
                adaptive=True, 
                bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
                content=ft.Row(
                    [
                        ft.Icon(name=ft.icons.MONEY, color="yellow"),
                        ft.Text("金", size=20, color="black", italic=True),
                    ],
                    tight=True,
                    ),
                     on_click=lambda e: button_clicked("金"),
            ))
    images.controls.append(
            ft.ElevatedButton(
                adaptive=True, 
                bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
                content=ft.Row(
                    [
                        ft.Icon(name=ft.icons.FOREST, color="green"),
                        ft.Text("木",size=20, color="black", italic=True),
                    ],
                    tight=True,
                    ),
                    on_click=lambda e: button_clicked("木"),
            ))
    images.controls.append(
            ft.ElevatedButton(
                adaptive=True, 
                bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
                content=ft.Row(
                    [
                        ft.Icon(name=ft.icons.WATER, color="blue"),
                        ft.Text("水",size=20, color="black", italic=True),
                    ],
                    tight=True,
                    ),
                    on_click=lambda e: button_clicked("水")
            ))
    images.controls.append(
            ft.ElevatedButton(
            adaptive=True, 
            bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.FIRE_HYDRANT, color="red"),
                    ft.Text("火",size=20, color="black", italic=True),
                ],
                tight=True,
                ),
                on_click=lambda e: button_clicked("火")
            ))
    images.controls.append(
            ft.ElevatedButton(
            adaptive=True, 
            bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.EARBUDS_BATTERY_SHARP, color="brown"),
                    ft.Text("土",size=20, color="black", italic=True),
                ],
                tight=True,
                ),
                on_click=lambda e: button_clicked("土")
            ))
    images.controls.append(
            ft.ElevatedButton(
            adaptive=True, 
            bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.FACE, color="grey"),
                    ft.Text("兄弟",size=20, color="black", italic=True),
                ],
                tight=True,
                ),
                on_click=lambda e: button_clicked("兄弟")
            ))
    images.controls.append(
            ft.ElevatedButton(
            adaptive=True, 
            bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.AIR, color="white"),
                    ft.Text("好香",size=20, color="black", italic=True),
                ],
                tight=True,
                ),
                on_click=lambda e: button_clicked("好香")
            ))
    images.controls.append(
            ft.ElevatedButton(
            adaptive=True, 
            bgcolor=ft.cupertino_colors.SYSTEM_TEAL,
            content=ft.Row(
                [
                    ft.Icon(name=ft.icons.SPACE_BAR, color="green"),
                    ft.Text("......",size=20, color="black", italic=True),
                ],
                tight=True,
                ),
                on_click=lambda e: button_clicked("......")
            ))
    Side_tab = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    Hint_text = ft.Text('请选择两个词语进行合成：',theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM)
    Intro_text = ft.Text('',theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM)
    Info_text = ft.Text('',theme_style=ft.TextThemeStyle.BODY_LARGE)
    Side_tab.controls.append(Hint_text)
    Side_tab.controls.append(Intro_text)
    Side_tab.controls.append(Info_text)
    page.add(ft.Row([images,Side_tab]))

ft.app(target=main, view=ft.WEB_BROWSER, port=8800, web_renderer='html')

# async def main(page: ft.Page):
#     async def button_clicked(param):
#         global cnt
#         global prompt
#         if cnt == 0:
#             cnt = cnt + 1
#             prompt = param
#         else:
#             cnt = 0
#             prompt = prompt + '+' + param
#             print('Begin: '+prompt)
#             response, history = model.chat(tokenizer, prompt, history=history_init)
#             print(response)
#             await page.add_async(ft.ElevatedButton(text=response, on_click=lambda e: button_clicked(response)))
#             await page.update_async()
        
#     await page.add_async(
#         ft.ElevatedButton(text="金",on_click=lambda e: button_clicked("金")),
#         ft.ElevatedButton(text="木",on_click=lambda e: button_clicked("木")),
#         ft.ElevatedButton(text="水",on_click=lambda e: button_clicked("水")),
#         ft.ElevatedButton(text="火",on_click=lambda e: button_clicked("火")),
#         ft.ElevatedButton(text="土",on_click=lambda e: button_clicked("土")),
#     )



# app = flet_fastapi.app(main)

# ! TODO:
# ! 1. Add Cache
# X 2. Change to word card
# ! 3. Add regex
# ! 4. Add Waiting feedback
# ! 5. Add Sound Effect