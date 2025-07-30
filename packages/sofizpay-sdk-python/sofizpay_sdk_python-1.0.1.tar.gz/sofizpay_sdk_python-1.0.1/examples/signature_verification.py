"""
مثال لاختبار التحقق من توقيع SofizPay
"""

import sys
import os

# إضافة مسار المشروع للوصول للمكتبة
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sofizpay import SofizPayClient


def test_signature_verification():
    """اختبار التحقق من التوقيع"""
    
    print("🔐 اختبار التحقق من توقيع SofizPay")
    print("=" * 50)
    
    # إنشاء عميل SofizPay
    client = SofizPayClient()
    
    # بيانات اختبار - يجب استبدالها ببيانات حقيقية من SofizPay
    test_cases = [
        {
            "name": "اختبار توقيع صحيح (مثال)",
            "data": {
                "message": "test_message_from_sofizpay",
                "signature_url_safe": "invalid_signature_for_testing"
            },
            "expected": False  # سيكون False لأن هذا توقيع وهمي
        },
        {
            "name": "اختبار رسالة فارغة",
            "data": {
                "message": "",
                "signature_url_safe": "some_signature"
            },
            "expected": False
        },
        {
            "name": "اختبار توقيع فارغ",
            "data": {
                "message": "test_message",
                "signature_url_safe": ""
            },
            "expected": False
        }
    ]
    
    print(f"📋 عدد الاختبارات: {len(test_cases)}")
    print()
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🧪 الاختبار #{i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            # تشغيل التحقق من التوقيع
            result = client.verify_sofizpay_signature(test_case['data'])
            
            print(f"📨 الرسالة: {test_case['data']['message'][:50]}...")
            print(f"🔏 التوقيع: {test_case['data']['signature_url_safe'][:30]}...")
            print(f"✅ النتيجة المتوقعة: {test_case['expected']}")
            print(f"📊 النتيجة الفعلية: {result}")
            
            if result == test_case['expected']:
                print("✅ الاختبار نجح!")
                success_count += 1
            else:
                print("❌ الاختبار فشل!")
                
        except Exception as e:
            print(f"❌ خطأ في الاختبار: {e}")
        
        print()
    
    print("📈 ملخص النتائج")
    print("=" * 30)
    print(f"✅ الاختبارات الناجحة: {success_count}/{len(test_cases)}")
    print(f"❌ الاختبارات الفاشلة: {len(test_cases) - success_count}/{len(test_cases)}")
    
    if success_count == len(test_cases):
        print("🎉 جميع الاختبارات نجحت!")
    else:
        print("⚠️ بعض الاختبارات فشلت")


def test_with_real_data():
    """اختبار مع بيانات حقيقية من SofizPay"""
    
    print("\n" + "=" * 60)
    print("🔐 اختبار مع بيانات حقيقية")
    print("=" * 60)
    
    # إنشاء عميل SofizPay
    client = SofizPayClient()
    
    print("📝 لاختبار التوقيع مع بيانات حقيقية:")
    print("1. احصل على رسالة موقعة من SofizPay")
    print("2. احصل على التوقيع URL-safe base64")
    print("3. استبدل القيم أدناه")
    print()
    
    # ضع هنا البيانات الحقيقية من SofizPay
    real_message = input("أدخل الرسالة الأصلية (أو اضغط Enter للتخطي): ").strip()
    
    if real_message:
        real_signature = input("أدخل التوقيع URL-safe base64: ").strip()
        
        if real_signature:
            print(f"\n🔍 التحقق من التوقيع...")
            print(f"📨 الرسالة: {real_message}")
            print(f"🔏 التوقيع: {real_signature[:50]}...")
            
            try:
                result = client.verify_sofizpay_signature({
                    "message": real_message,
                    "signature_url_safe": real_signature
                })
                
                if result:
                    print("✅ التوقيع صحيح!")
                else:
                    print("❌ التوقيع غير صحيح!")
                    
            except Exception as e:
                print(f"❌ خطأ في التحقق: {e}")
        else:
            print("⏭️ تم تخطي الاختبار - لم يتم إدخال توقيع")
    else:
        print("⏭️ تم تخطي الاختبار - لم يتم إدخال رسالة")


def show_sofizpay_public_key():
    """عرض المفتاح العام لـ SofizPay"""
    
    print("\n" + "=" * 60)
    print("🔑 المفتاح العام لـ SofizPay")
    print("=" * 60)
    
    print("هذا هو المفتاح العام المستخدم للتحقق من توقيع SofizPay:")
    print()
    print(SofizPayClient.SOFIZPAY_PUBLIC_KEY_PEM)
    print()
    print("💡 نصائح:")
    print("- هذا المفتاح مدمج في SDK")
    print("- يستخدم لتأكيد أن الرسائل أتت من SofizPay")
    print("- لا تحتاج لتعديله أو تغييره")


if __name__ == "__main__":
    print("🏦 مثال التحقق من توقيع SofizPay")
    print("=" * 50)
    
    try:
        # تشغيل الاختبارات الأساسية
        test_signature_verification()
        
        # عرض المفتاح العام
        show_sofizpay_public_key()
        
        # اختبار مع بيانات حقيقية
        test_with_real_data()
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()
