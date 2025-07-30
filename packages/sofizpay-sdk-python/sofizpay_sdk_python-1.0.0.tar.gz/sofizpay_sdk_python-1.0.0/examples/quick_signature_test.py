"""
اختبار سريع لوظيفة التحقق من التوقيع
"""

import sys
import os

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sofizpay import SofizPayClient


def quick_test():
    """اختبار سريع للوظيفة"""
    
    print("🔐 اختبار سريع لـ verify_sofizpay_signature")
    print("=" * 50)
    
    # إنشاء العميل
    client = SofizPayClient()
    
    # عرض المفتاح العام المستخدم
    print("🔑 المفتاح العام المستخدم:")
    print(client.SOFIZPAY_PUBLIC_KEY_PEM[:100] + "...")
    print()
    
    # اختبار مع بيانات وهمية
    print("🧪 اختبار مع بيانات وهمية:")
    
    test_data = {
        "message": "test_message_hello_world",
        "signature_url_safe": "fake_signature_123"
    }
    
    print(f"📨 الرسالة: {test_data['message']}")
    print(f"🔏 التوقيع: {test_data['signature_url_safe']}")
    
    try:
        result = client.verify_sofizpay_signature(test_data)
        print(f"📊 النتيجة: {result}")
        
        if result:
            print("✅ التوقيع صحيح")
        else:
            print("❌ التوقيع غير صحيح (متوقع لأنه وهمي)")
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    print("\n" + "=" * 50)
    print("💡 لاختبار التوقيع مع بيانات حقيقية:")
    print("1. احصل على رسالة من SofizPay")
    print("2. احصل على التوقيع المقابل")
    print("3. استخدم الكود التالي:")
    print()
    print("client = SofizPayClient()")
    print("result = client.verify_sofizpay_signature({")
    print('    "message": "your_real_message",')
    print('    "signature_url_safe": "your_real_signature"')
    print("})")
    print("print(f'Valid: {result}')")


if __name__ == "__main__":
    quick_test()
