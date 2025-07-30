"""
اختبارات متقدمة لوظيفة التحقق من التوقيع في SofizPay
"""

import base64
import sys
import os

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sofizpay import SofizPayClient


class SignatureTestSuite:
    """مجموعة اختبارات شاملة للتوقيع"""
    
    def __init__(self):
        self.client = SofizPayClient()
        self.test_results = []
    
    def run_test(self, test_name: str, test_func):
        """تشغيل اختبار واحد وتسجيل النتيجة"""
        print(f"\n🧪 {test_name}")
        print("-" * 50)
        
        try:
            result = test_func()
            self.test_results.append({
                'name': test_name,
                'status': 'نجح' if result else 'فشل',
                'success': result
            })
            print(f"✅ النتيجة: {'نجح' if result else 'فشل'}")
            
        except Exception as e:
            self.test_results.append({
                'name': test_name,
                'status': f'خطأ: {str(e)}',
                'success': False
            })
            print(f"❌ خطأ: {e}")
    
    def test_empty_message(self):
        """اختبار رسالة فارغة"""
        result = self.client.verify_sofizpay_signature({
            "message": "",
            "signature_url_safe": "test_signature"
        })
        return result == False  # يجب أن يعيد False
    
    def test_empty_signature(self):
        """اختبار توقيع فارغ"""
        result = self.client.verify_sofizpay_signature({
            "message": "test_message",
            "signature_url_safe": ""
        })
        return result == False  # يجب أن يعيد False
    
    def test_missing_message(self):
        """اختبار رسالة مفقودة"""
        result = self.client.verify_sofizpay_signature({
            "signature_url_safe": "test_signature"
        })
        return result == False  # يجب أن يعيد False
    
    def test_missing_signature(self):
        """اختبار توقيع مفقود"""
        result = self.client.verify_sofizpay_signature({
            "message": "test_message"
        })
        return result == False  # يجب أن يعيد False
    
    def test_invalid_base64_signature(self):
        """اختبار توقيع base64 غير صحيح"""
        result = self.client.verify_sofizpay_signature({
            "message": "test_message",
            "signature_url_safe": "invalid_base64_!"
        })
        return result == False  # يجب أن يعيد False
    
    def test_url_safe_conversion(self):
        """اختبار تحويل URL-safe base64"""
        # إنشاء توقيع وهمي مع أحرف URL-safe
        fake_signature = "abc-def_ghi"  # يحتوي على - و _
        
        result = self.client.verify_sofizpay_signature({
            "message": "test_message",
            "signature_url_safe": fake_signature
        })
        return result == False  # يجب أن يعيد False لأنه توقيع وهمي
    
    def test_arabic_message(self):
        """اختبار رسالة بالعربية"""
        result = self.client.verify_sofizpay_signature({
            "message": "رسالة تجريبية باللغة العربية",
            "signature_url_safe": "fake_signature_123"
        })
        return result == False  # يجب أن يعيد False لأنه توقيع وهمي
    
    def test_long_message(self):
        """اختبار رسالة طويلة"""
        long_message = "a" * 1000  # رسالة من 1000 حرف
        result = self.client.verify_sofizpay_signature({
            "message": long_message,
            "signature_url_safe": "fake_signature_123"
        })
        return result == False  # يجب أن يعيد False لأنه توقيع وهمي
    
    def test_typical_cib_message(self):
        """اختبار رسالة CIB نموذجية"""
        cib_message = "wc_order_LI3SLQ7xA7IY9cib84907success23400"
        result = self.client.verify_sofizpay_signature({
            "message": cib_message,
            "signature_url_safe": "fake_signature_for_cib_test"
        })
        return result == False  # يجب أن يعيد False لأنه توقيع وهمي
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🔐 بدء مجموعة اختبارات التوقيع المتقدمة")
        print("=" * 60)
        
        # قائمة الاختبارات
        tests = [
            ("اختبار رسالة فارغة", self.test_empty_message),
            ("اختبار توقيع فارغ", self.test_empty_signature),
            ("اختبار رسالة مفقودة", self.test_missing_message),
            ("اختبار توقيع مفقود", self.test_missing_signature),
            ("اختبار base64 غير صحيح", self.test_invalid_base64_signature),
            ("اختبار تحويل URL-safe", self.test_url_safe_conversion),
            ("اختبار رسالة عربية", self.test_arabic_message),
            ("اختبار رسالة طويلة", self.test_long_message),
            ("اختبار رسالة CIB نموذجية", self.test_typical_cib_message),
        ]
        
        # تشغيل كل اختبار
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # عرض النتائج النهائية
        self.show_summary()
    
    def show_summary(self):
        """عرض ملخص النتائج"""
        print("\n" + "=" * 60)
        print("📊 ملخص نتائج الاختبارات")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"📈 إجمالي الاختبارات: {total_tests}")
        print(f"✅ الاختبارات الناجحة: {successful_tests}")
        print(f"❌ الاختبارات الفاشلة: {failed_tests}")
        print(f"📊 نسبة النجاح: {(successful_tests/total_tests)*100:.1f}%")
        
        print("\n📋 تفاصيل النتائج:")
        for i, result in enumerate(self.test_results, 1):
            status_icon = "✅" if result['success'] else "❌"
            print(f"{status_icon} {i}. {result['name']}: {result['status']}")
        
        if successful_tests == total_tests:
            print("\n🎉 تهانينا! جميع الاختبارات نجحت!")
        else:
            print(f"\n⚠️ {failed_tests} اختبار(ات) فشلت - راجع التفاصيل أعلاه")


def show_usage_example():
    """عرض مثال للاستخدام"""
    print("\n" + "=" * 60)
    print("📖 مثال الاستخدام")
    print("=" * 60)
    
    code_example = '''
# إنشاء عميل SofizPay
client = SofizPayClient()

# بيانات التحقق (من SofizPay webhook أو API response)
verification_data = {
    "message": "wc_order_ABC123_success_100.50",
    "signature_url_safe": "jHrONYl2NuBhjAYTgRq3xwRuW2ZYZIQlx1..."
}

# التحقق من التوقيع
is_valid = client.verify_sofizpay_signature(verification_data)

if is_valid:
    print("✅ التوقيع صحيح - الرسالة من SofizPay")
else:
    print("❌ التوقيع غير صحيح - احتمال تلاعب")
'''
    
    print("💻 كود المثال:")
    print(code_example)
    
    print("📝 ملاحظات مهمة:")
    print("• الرسالة يجب أن تكون نفس الرسالة الأصلية المرسلة من SofizPay")
    print("• التوقيع يجب أن يكون مشفر بـ URL-safe base64")
    print("• الدالة تستخدم المفتاح العام المدمج في SDK")
    print("• تعيد True فقط إذا كان التوقيع صحيح ومن SofizPay")


def interactive_test():
    """اختبار تفاعلي"""
    print("\n" + "=" * 60)
    print("🎮 اختبار تفاعلي")
    print("=" * 60)
    
    client = SofizPayClient()
    
    print("أدخل بيانات التحقق لاختبارها:")
    
    while True:
        print("\n" + "-" * 40)
        message = input("📨 الرسالة (أو 'exit' للخروج): ").strip()
        
        if message.lower() == 'exit':
            print("👋 وداعاً!")
            break
        
        if not message:
            print("⚠️ يرجى إدخال رسالة")
            continue
        
        signature = input("🔏 التوقيع URL-safe base64: ").strip()
        
        if not signature:
            print("⚠️ يرجى إدخال توقيع")
            continue
        
        print("\n🔍 جاري التحقق...")
        
        try:
            result = client.verify_sofizpay_signature({
                "message": message,
                "signature_url_safe": signature
            })
            
            if result:
                print("✅ التوقيع صحيح!")
            else:
                print("❌ التوقيع غير صحيح!")
                
        except Exception as e:
            print(f"❌ خطأ في التحقق: {e}")


if __name__ == "__main__":
    print("🏦 اختبارات متقدمة لتوقيع SofizPay")
    print("=" * 60)
    
    try:
        # تشغيل مجموعة الاختبارات المتقدمة
        test_suite = SignatureTestSuite()
        test_suite.run_all_tests()
        
        # عرض مثال الاستخدام
        show_usage_example()
        
        # اختبار تفاعلي
        if input("\n🎮 هل تريد تجربة الاختبار التفاعلي؟ (y/n): ").lower() == 'y':
            interactive_test()
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف الاختبار")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()
