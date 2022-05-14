from unittest import result
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.template.context_processors import csrf
from django.views.generic import FormView

import math
from . import forms
from .food_menu import Normal_menu, Diet_menu, Increase_menu
from .workout_menu import Bulkup_workout, Normal_workout, Diet_workout

class Result(FormView):
    """選択されたデータをもとに、期間、食事、トレーニングを生成するクラス"""

    form_class = forms.SelectForm
    template_name = 'workout/result.html'
    success_url = 'result'

    def form_valid(self, form):
        """formから受け取ったデータを一つずつ、取り出し、
        それぞれ最適な答えを導き出した後、viewに返す
        """

        data = form.cleaned_data
        sex = data['sex']
        goal = data['goal']
        old = data['old']
        height = data['height']
        weight = data['weight'] 
        
        # 年齢、身長、体重を数値に変換
        old = int(old)
        height = int(height)
        weight = int(weight)

        # 男性の目標体重を計算
        if sex == 'men':
            
            # スマート体型の目標体重を生成
            if goal == 'smart':
                goal_weight = (height / 100)**2 
                goal_weight *= 20

            # ガッチリ体型の目標体重を生成
            else:
                goal_weight = (height / 100)**2
                goal_weight *= 24

        # 女性の目標体重を計算
        else:
            # スマート体型の目標体重を生成
            if goal == 'smart':
                goal_weight = (height / 100)**2 
                goal_weight *= 18

            # ガッチリ体型の目標体重を生成
            else:
                goal_weight = (height / 100)**2
                goal_weight *= 22
        
        # 目標体重の小数点を切り捨て
        goal_weight = round(goal_weight)

        # 期間を代入
        period = 0

        # 目標体重の方が、重い場合の期間を生成
        if weight < goal_weight:
            # 期間は,(期間(ヶ月)=目標体重-現体重)とする(無理なく増量するには、1ヶ月1キロと目安にされている)
            period = goal_weight - weight

            # 期間が3以下の場合、一律で3とする(体作りには、最低限3ヶ月必要なため)
            if period < 3:
                period = str(3) + 'ヶ月'

            # 期間が12の場合、[1年]と表示されるようにする
            elif 12 == period:
                period = str(1) + '年'

            # 期間が24の場合、[2年]と表示されるようにする
            elif 24 == period:
                period = str(2) + '年'

            # 期間が12から24以内の場合、[1年ヶ月]と表示させる
            elif 12 < period < 24:
                month = period - 12
                period = 1
                period = str(period) + '年' + str(month) + 'ヶ月'

            # 期間が24以上の場合、[2年ヶ月]と表示させる
            elif 24 < period:
                month = period - 24
                period = 2
                period = str(period) + '年' + str(month) + 'ヶ月'

            # 期間が3以上12以内の場合、[ヶ月]と表示
            else:
                period = str(period) + 'ヶ月'   

        # 目標体重と現体重が同一の場合の、期間を生成
        elif weight == goal_weight:
            # 同一の場合、一律で3ヶ月とする(体作りには、最低限3ヶ月必要なため)
            period = str(3) + 'ヶ月'

        # 目標体重の方が、低い場合の期間を生成
        else:
            period = (weight - goal_weight) / 2
            period = math.ceil(period)

            # 期間が3以下の場合、一律で3とする(体作りには、最低限3ヶ月必要なため)
            if period < 3:
                period = str(3) + 'ヶ月'

            # 期間が12の場合、[1年]と表示されるようにする
            elif 12 == period:
                period = str(1) + '年'

            # 期間が24の場合、[2年]と表示されるようにする
            elif 24 == period:
                period = str(2) + '年'

            # 期間が12から24以内の場合、[1年ヶ月]と表示させる
            elif 12 < period < 24:
                month = period - 12
                period = 1
                period = str(period) + '年' + str(month) + 'ヶ月'

            # 期間が24以上の場合、[2年ヶ月]と表示させる
            elif 24 < period:
                month = period - 24
                period = 2
                period = str(period) + '年' + str(month) + 'ヶ月'

            # 期間が3以上12以内の場合、[ヶ月]と表示
            else:
                period = str(period) + 'ヶ月'

        # 食事メニューの生成
        # 増量が必要な場合の、食事を生成
        if weight < goal_weight:

            # 朝食の生成
            morning_main = Increase_menu.morning_main
            morning_menu01 = Increase_menu.morning_menu_01
            morning_menu02 = Increase_menu.morning_menu_02
            morning_menu03 = Increase_menu.morning_menu_03
            morning_menu04 = Increase_menu.morning_menu_04
            morning_menu05 = Increase_menu.morning_menu_05

            # 昼食の生成
            lunch_main = Increase_menu.lunch_main
            lunch_menu01 = Increase_menu.lunch_menu_01
            lunch_menu02 = Increase_menu.lunch_menu_02
            lunch_menu03 = Increase_menu.lunch_menu_03
            lunch_menu04 = Increase_menu.lunch_menu_04
            lunch_menu05 = Increase_menu.lunch_menu_05

            # 夕食の生成
            dinner_main = Increase_menu.dinner_main
            dinner_menu01 = Increase_menu.dinner_menu_01
            dinner_menu02 = Increase_menu.dinner_menu_02
            dinner_menu03 = Increase_menu.dinner_menu_03
            dinner_menu04 = Increase_menu.dinner_menu_04
            dinner_menu05 = Increase_menu.dinner_menu_05

            # 間食の生成
            snack01 = Increase_menu.snack_01
            snack02 = Increase_menu.snack_02
            snack03 = Increase_menu.snack_03

        # 現体重と目標体重が同一の場合の食事を生成
        elif weight == goal_weight:

            # 朝食の生成
            morning_main = Normal_menu.morning_main
            morning_menu01 = Normal_menu.morning_menu_01
            morning_menu02 = Normal_menu.morning_menu_02
            morning_menu03 = Normal_menu.morning_menu_03
            morning_menu04 = Normal_menu.morning_menu_04
            morning_menu05 = Normal_menu.morning_menu_05

            # 昼食の生成
            lunch_main = Normal_menu.lunch_main
            lunch_menu01 = Normal_menu.lunch_menu_01
            lunch_menu02 = Normal_menu.lunch_menu_02
            lunch_menu03 = Normal_menu.lunch_menu_03
            lunch_menu04 = Normal_menu.lunch_menu_04
            lunch_menu05 = Normal_menu.lunch_menu_05

            # 夕食の生成
            dinner_main = Normal_menu.dinner_main
            dinner_menu01 = Normal_menu.dinner_menu_01
            dinner_menu02 = Normal_menu.dinner_menu_02
            dinner_menu03 = Normal_menu.dinner_menu_03
            dinner_menu04 = Normal_menu.dinner_menu_04
            dinner_menu05 = Normal_menu.dinner_menu_05

            # 間食の生成
            snack01 = Normal_menu.snack_01
            snack02 = Normal_menu.snack_02
            snack03 = Normal_menu.snack_03

        # 減量が必要な場合の、食事を生成
        else:

            # 朝食の生成
            morning_main = Diet_menu.morning_main
            morning_menu01 = Diet_menu.morning_menu_01
            morning_menu02 = Diet_menu.morning_menu_02
            morning_menu03 = Diet_menu.morning_menu_03
            morning_menu04 = Diet_menu.morning_menu_04
            morning_menu05 = Diet_menu.morning_menu_05

            # 昼食の生成
            lunch_main = Diet_menu.lunch_main
            lunch_menu01 = Diet_menu.lunch_menu_01
            lunch_menu02 = Diet_menu.lunch_menu_02
            lunch_menu03 = Diet_menu.lunch_menu_03
            lunch_menu04 = Diet_menu.lunch_menu_04
            lunch_menu05 = Diet_menu.lunch_menu_05

            # 夜食の生成
            dinner_main = Diet_menu.dinner_main
            dinner_menu01 = Diet_menu.dinner_menu_01
            dinner_menu02 = Diet_menu.dinner_menu_02
            dinner_menu03 = Diet_menu.dinner_menu_03
            dinner_menu04 = Diet_menu.dinner_menu_04
            dinner_menu05 = Diet_menu.dinner_menu_05

            # 間食の生成
            snack01 = Diet_menu.snack_01
            snack02 = Diet_menu.snack_02
            snack03 = Diet_menu.snack_03

        # トレーニングメニューの生成
        # ガッチリ体型用のトレーニング
        if weight < goal_weight:
            # index.htmlの表示を分岐するための変数
            workout_type = 'big'

            # 胸筋メニュー
            breast_title = Bulkup_workout.breast_title
            breast_menu = Bulkup_workout.breast_menu
            breast_rep = Bulkup_workout.breast_rep
            breast_set = Bulkup_workout.breast_set

            # 肩メニュー
            sholder_title = Bulkup_workout.sholder_title
            sholder_menu = Bulkup_workout.sholder_menu
            sholder_rep = Bulkup_workout.sholder_rep
            sholder_set = Bulkup_workout.sholder_set

            # 背筋メニュー
            back_title = Bulkup_workout.back_title
            back_menu = Bulkup_workout.back_menu
            back_rep = Bulkup_workout.back_rep
            back_set = Bulkup_workout.back_set

            # 腕メニュー1
            arm01_title = Bulkup_workout.arm01_title
            arm01_menu = Bulkup_workout.arm01_menu
            arm01_rep = Bulkup_workout.arm01_rep
            arm01_set = Bulkup_workout.arm01_set

            # 腕メニュー2
            arm02_title = Bulkup_workout.arm02_title
            arm02_menu = Bulkup_workout.arm02_menu
            arm02_rep = Bulkup_workout.arm02_rep
            arm02_set = Bulkup_workout.arm02_set

            # 脚メニュー1
            reg01_title = Bulkup_workout.reg01_title
            reg01_menu = Bulkup_workout.reg01_menu
            reg01_rep = Bulkup_workout.reg01_rep
            reg01_set = Bulkup_workout.reg01_set

            # 脚メニュー2
            reg02_title = Bulkup_workout.reg02_title
            reg02_menu = Bulkup_workout.reg02_menu
            reg02_rep = Bulkup_workout.reg02_rep
            reg02_set = Bulkup_workout.reg02_set

            # 他体型用のメニューを、空の変数に格納(エラーを起こさないため)
            run_title = run_menu = run_rep = run_set = ''
            abs01_title = abs01_menu = abs01_rep = abs01_set = ''
            abs02_title = abs02_menu = abs02_rep = abs02_set = ''
            waist01_title = waist01_menu = waist01_rep = waist01_set = ''
            waist02_title = waist02_menu = waist02_rep = waist02_set = ''

        # 体型維持用のトレーニング
        elif weight == goal_weight:
            # index.htmlの表示を分岐するための変数
            workout_type = 'normal'

            # 胸筋メニュー
            breast_title = Normal_workout.breast_title
            breast_menu = Normal_workout.breast_menu
            breast_rep = Normal_workout.breast_rep
            breast_set = Normal_workout.breast_set

            # 肩メニュー
            sholder_title = Normal_workout.sholder_title
            sholder_menu = Normal_workout.sholder_menu
            sholder_rep = Normal_workout.sholder_rep
            sholder_set = Normal_workout.sholder_set

            # 背筋メニュー
            back_title = Normal_workout.back_title
            back_menu = Normal_workout.back_menu
            back_rep = Normal_workout.back_rep
            back_set = Normal_workout.back_set

            # 腕メニュー
            arm01_title = Normal_workout.arm01_title
            arm01_menu = Normal_workout.arm01_menu
            arm01_rep = Normal_workout.arm01_rep
            arm01_set = Normal_workout.arm01_set

            # 脚メニュー
            reg01_title = Normal_workout.reg01_title
            reg01_menu = Normal_workout.reg01_menu
            reg01_rep = Normal_workout.reg01_rep
            reg01_set = Normal_workout.reg01_set

            # 有酸素メニュー
            run_title = Normal_workout.run_title
            run_menu = Normal_workout.run_menu
            run_rep = Normal_workout.run_rep
            run_set = Normal_workout.run_set

            # 他体型用のメニューを、空の変数に格納(エラーを起こさないため)
            reg02_title = reg02_menu = reg02_rep = reg02_set = ''
            arm02_title = arm02_menu = arm02_rep = arm02_set = ''
            abs01_title = abs01_menu = abs01_rep = abs01_set = ''
            abs02_title = abs02_menu = abs02_rep = abs02_set = ''
            waist01_title = waist01_menu = waist01_rep = waist01_set = ''
            waist02_title = waist02_menu = waist02_rep = waist02_set = ''

        # ダイエット用のトレーニング
        else:
            # index.htmlの表示を分岐するための変数
            workout_type = 'diet'

            # 腹筋メニュー1
            abs01_title = Diet_workout.abs01_title
            abs01_menu = Diet_workout.abs01_menu
            abs01_rep = Diet_workout.abs01_rep
            abs01_set = Diet_workout.abs01_set

            # 腹筋メニュー1
            abs02_title = Diet_workout.abs02_title
            abs02_menu = Diet_workout.abs02_menu
            abs02_rep = Diet_workout.abs02_rep
            abs02_set = Diet_workout.abs02_set

            # 背筋メニュー
            back_title = Diet_workout.back_title
            back_menu = Diet_workout.back_menu
            back_rep = Diet_workout.back_rep
            back_set = Diet_workout.back_set

            # ウエストメニュー1
            waist01_title = Diet_workout.waist01_title
            waist01_menu = Diet_workout.waist01_menu
            waist01_rep = Diet_workout.waist01_rep
            waist01_set = Diet_workout.waist01_set

            # ウエストメニュー2
            waist02_title = Diet_workout.waist02_title
            waist02_menu = Diet_workout.waist02_menu
            waist02_rep = Diet_workout.waist02_rep
            waist02_set = Diet_workout.waist02_set
        
            # 脚メニュー
            reg01_title = Diet_workout.reg01_title
            reg01_menu = Diet_workout.reg01_menu
            reg01_rep = Diet_workout.reg01_rep
            reg01_set = Diet_workout.reg01_set

            # 有酸素メニュー
            run_title = Diet_workout.run_title
            run_menu = Diet_workout.run_menu
            run_rep = Diet_workout.run_rep
            run_set = Diet_workout.run_set

            # 他体型用のメニューを、空の変数に格納(エラーを起こさないため)
            sholder_title = sholder_menu = sholder_rep = sholder_set = ''
            breast_title = breast_menu = breast_rep = breast_set = ''
            reg02_title = reg02_menu = reg02_rep = reg02_set = ''
            arm01_title = arm01_menu = arm01_rep = arm01_set = ''
            arm02_title = arm02_menu = arm02_rep = arm02_set = ''

        # 増量用の参考動画を生成
        if weight < goal_weight:

            # 男性増量用の食事とトレーニング動画を生成
            if sex == 'men':
                meal_video01 = 'https://www.youtube.com/embed/MaTfN65r8uU'
                meal_video02 = 'https://www.youtube.com/embed/vKOiTxoCn94'
                meal_video03 = 'https://www.youtube.com/embed/2BWnXBWGulQ'

                workout_video01 = 'https://www.youtube.com/embed/DBDlEDN7ZB8'
                workout_video02 = 'https://www.youtube.com/embed/Ud90ULSFuYc'
                workout_video03 = 'https://www.youtube.com/embed/vaWma9yX0CQ'

            # 女性増量用の食事とトレーニング動画を生成
            else:
                meal_video01 = 'https://www.youtube.com/embed/wcvErL4rqWc'
                meal_video02 = 'https://www.youtube.com/embed/nDCDRXQlusc'
                meal_video03 = 'https://www.youtube.com/embed/BxpeOq18c08'

                workout_video01 = 'https://www.youtube.com/embed/QDh498hTYnc'
                workout_video02 = 'https://www.youtube.com/embed/X_dUYiIuxeo'
                workout_video03 = 'https://www.youtube.com/embed/upbMaKNR4Sg'

        # 体型維持用の参考動画を生成
        elif weight == goal_weight:

            # 男性体型維持用の食事とトレーニング動画を生成
            if sex == 'men':
                meal_video01 = 'https://www.youtube.com/embed/zD1_xYBLw40'
                meal_video02 = 'https://www.youtube.com/embed/qzZA3cHBV1U'
                meal_video03 = 'https://www.youtube.com/embed/V6H3uJ1E0-M'

                workout_video01 = 'https://www.youtube.com/embed/PchdWhx3w7Q'
                workout_video02 = 'https://www.youtube.com/embed/2pMi6ZbxSRo'
                workout_video03 = 'https://www.youtube.com/embed/1mtXFf0C6g4'

            # 女性体型維持用の食事とトレーニング動画を生成
            else:
                meal_video01 = 'https://www.youtube.com/embed/_W9NOw9cMXA'
                meal_video02 = 'https://www.youtube.com/embed/NkG4aRgOqIg'
                meal_video03 = 'https://www.youtube.com/embed/twlgKyt78Ac'

                workout_video01 = 'https://www.youtube.com/embed/QDh498hTYnc'
                workout_video02 = 'https://www.youtube.com/embed/gH9k2AZxf6k'
                workout_video03 = 'https://www.youtube.com/embed/upbMaKNR4Sg'

        # 減量用の参考動画を生成
        else:

            # 男性減量用の食事とトレーニング動画を生成
            if sex == 'men':
                meal_video01 = 'https://www.youtube.com/embed/lScKFPP8hg4'
                meal_video02 = 'https://www.youtube.com/embed/ZShBuR3tayQ'
                meal_video03 = 'https://www.youtube.com/embed/XCy2NkUosW0'

                workout_video01 = 'https://www.youtube.com/embed/hns0ZEl3fVY'
                workout_video02 = 'https://www.youtube.com/embed/2pMi6ZbxSRo'
                workout_video03 = 'https://www.youtube.com/embed/joNzM16CASk'

            # 女性減量用の食事とトレーニング動画を生成
            else:
                meal_video01 = 'https://www.youtube.com/embed/CmHQzvjrwt8'
                meal_video02 = 'https://www.youtube.com/embed/kyU-wC9SylI'
                meal_video03 = 'https://www.youtube.com/embed/8OnYhyzJdb0'

                workout_video01 = 'https://www.youtube.com/embed/pBo_DjHqVws'
                workout_video02 = 'https://www.youtube.com/embed/gH9k2AZxf6k'
                workout_video03 = 'https://www.youtube.com/embed/Ve0ZjODJjQ0'

        # 性別毎に背景画像を分岐
        if sex == 'men':
            sex_content = 'men-content'

        else:
            sex_content = 'women-content'    

        # 目標体重との差分体重
        diff_weight = goal_weight - weight
        result_diff = ''
        if diff_weight == 0:
            result_diff = '現体重をキープ'
        
        elif 0 < diff_weight:
            result_diff = '+' + str(diff_weight) + 'kg'

        else:
            result_diff = str(diff_weight) + 'kg'        

        # 生成したデータを、tmpに返せるdict型に変換
        ctxt = self.get_context_data(period=period, goal_weight=goal_weight, result_diff=result_diff,
                                     morning_main=morning_main, morning_menu01=morning_menu01, morning_menu02=morning_menu02, morning_menu03=morning_menu03, morning_menu04=morning_menu04, morning_menu05=morning_menu05, 
                                     lunch_main=lunch_main, lunch_menu01=lunch_menu01, lunch_menu02=lunch_menu02, lunch_menu03=lunch_menu03, lunch_menu04=lunch_menu04, lunch_menu05=lunch_menu05,
                                     dinner_main=dinner_main, dinner_menu01=dinner_menu01, dinner_menu02=dinner_menu02, dinner_menu03=dinner_menu03, dinner_menu04=dinner_menu04, dinner_menu05=dinner_menu05,
                                     snack01=snack01, snack02=snack02, snack03=snack03,
                                     breast_title=breast_title, breast_menu=breast_menu, breast_rep=breast_rep, breast_set=breast_set,
                                     sholder_title=sholder_title, sholder_menu=sholder_menu, sholder_rep=sholder_rep, sholder_set=sholder_set,
                                     back_title=back_title, back_menu=back_menu, back_rep=back_rep, back_set=back_set,
                                     arm01_title=arm01_title, arm01_menu=arm01_menu, arm01_rep=arm01_rep, arm01_set=arm01_set,
                                     arm02_title=arm02_title, arm02_menu=arm02_menu, arm02_rep=arm02_rep, arm02_set=arm02_set,
                                     reg01_title=reg01_title, reg01_menu=reg01_menu, reg01_rep=reg01_rep, reg01_set=reg01_set,
                                     reg02_title=reg02_title, reg02_menu=reg02_menu, reg02_rep=reg02_rep, reg02_set=reg02_set,
                                     run_title=run_title, run_menu=run_menu, run_rep=run_rep, run_set=run_set,
                                     abs01_title=abs01_title, abs01_menu=abs01_menu, abs01_rep=abs01_rep, abs01_set=abs01_set,
                                     abs02_title=abs02_title, abs02_menu=abs02_menu, abs02_rep=abs02_rep, abs02_set=abs02_set,
                                     waist01_title=waist01_title, waist01_menu=waist01_menu, waist01_rep=waist01_rep, waist01_set=waist01_set,
                                     waist02_title=waist02_title, waist02_menu=waist02_menu, waist02_rep=waist02_rep, waist02_set=waist02_set,
                                     meal_video01=meal_video01, meal_video02=meal_video02, meal_video03=meal_video03,
                                     workout_video01=workout_video01, workout_video02=workout_video02, workout_video03=workout_video03,  
                                    sex_content=sex_content, workout_type=workout_type, form=form)

        # 生成した結果をdict型でtmpに返す
        return self.render_to_response(ctxt)

class Index(FormView):
    """indexページに表示する内容をformから出力
    indexページで選択したデータをResultクラスでカスタム
    出来る様に、dict型に返す

    Args:
        FormView (dict): formのSelectForm

    Returns:
        dict: indexで入力したデータ
    """

    form_class = forms.SelectForm
    template_name = 'workout/index.html'

    def form_valid(self, form):
        """入力されたデータをバリデーションする"""

        # form.cleaned_dataにフォームの入力内容が格納
        data = form.cleaned_data
        goal = data['goal']
        sex = data['sex']
        old = data['old']
        height = data['height']
        weight = data['weight']

        # テンプレートに渡す
        ctxt = self.get_context_data(goal=goal, sex=sex, old=old, height=height, weight=weight,
                                     form=form)                           
        return self.render_to_response(ctxt)