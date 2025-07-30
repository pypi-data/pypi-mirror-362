"""
مثال لاستخدام معاملات CIB والتحقق من التوقيع باستخدام SofizPay SDK
"""

import asyncio
from sofizpay import SofizPayClient, ValidationError, NetworkError


async def cib_transaction_example():
    """مثال على إنشاء معاملة CIB"""
    client = SofizPayClient()
    
    # بيانات المعاملة (يجب استبدالها بالقيم الفعلية)
    transaction_data = {
        "account": "YOUR_ACCOUNT_ID_HERE",
        "amount": 250.75,
        "full_name": "أحمد محمد علي",
        "phone": "+213123456789",
        "email": "ahmed.mohammed@example.com",
        "memo": "دفع فاتورة الكهرباء - شهر يوليو 2025",
        "return_url": "https://mywebsite.com/payment-success"
    }
    
    try:
        print("🏦 بدء إنشاء معاملة CIB...")
        print(f"💰 المبلغ: {transaction_data['amount']} DZD")
        print(f"👤 العميل: {transaction_data['full_name']}")
        print(f"📧 البريد: {transaction_data['email']}")
        print(f"📱 الهاتف: {transaction_data['phone']}")
        print("-" * 50)
        
        result = await client.make_cib_transaction(transaction_data)
        
        if result['success']:
            print("✅ تم إنشاء معاملة CIB بنجاح!")
            print(f"📊 الحالة: {result['status']} - {result['status_text']}")
            print(f"⏰ الوقت: {result['timestamp']}")
            
            # طباعة بيانات الاستجابة
            if 'data' in result:
                print(f"📄 البيانات: {result['data']}")
            
            # طباعة عنوان URL المستخدم
            print(f"🔗 URL: {result['url']}")
            
        else:
            print("❌ فشل في إنشاء معاملة CIB!")
            print(f"🚫 الخطأ: {result['error']}")
            
            if 'status_code' in result:
                print(f"📊 رمز الحالة: {result['status_code']}")
                
        return result
        
    except ValidationError as e:
        print(f"❌ خطأ في التحقق من البيانات: {e}")
        return None
    except NetworkError as e:
        print(f"❌ خطأ في الشبكة: {e}")
        return None
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        return None


def signature_verification_example():
    """مثال على التحقق من توقيع SofizPay"""
    client = SofizPayClient()
    
    # بيانات التحقق من التوقيع (أمثلة)
    verification_examples = [
        {
            "name": "مثال صحيح",
            "data": {
                "message": "wc_order_LI3SLQ7xA7IY9cib84907success23400",
                "signature_url_safe": "jHrONYl2NuBhjAYTgRq3xwRuW2ZYZIQlx1VWgiObu5FrSnY78pQ-CV0pAjRKWAje-DDZHhvMvzIFSBE9rj87xsWymjWYVlyZmuVr-sDPSa-zWZRsyWJhdj0XPZir4skkDFWlhaWpwtLql0D7N5yw_zu67plVuhaPk4d_jOhn0O0qN3scROa1H1pIAPhIreQHu72-Bx4v2g-NGceFVpiAMyf2j2rvVthkg4o6adxY_E0-y_AJfnJdL1HhmWOBpFEUk6ziV1aFzSJIo-XpueJSFWpL7wrAsQ6shcLE3zQSZXJoXhdR7nr92-Y7SXgEE_a9kP_Q4uExJCWcaOcPkQ5Bgg=="
            }
        },
        {
            "name": "مثال خاطئ - رسالة محرفة",
            "data": {
                "message": "wc_order_WRONG_MESSAGE",
                "signature_url_safe": "jHrONYl2NuBhjAYTgRq3xwRuW2ZYZIQlx1VWgiObu5FrSnY78pQ-CV0pAjRKWAje-DDZHhvMvzIFSBE9rj87xsWymjWYVlyZmuVr-sDPSa-zWZRsyWJhdj0XPZir4skkDFWlhaWpwtLql0D7N5yw_zu67plVuhaPk4d_jOhn0O0qN3scROa1H1pIAPhIreQHu72-Bx4v2g-NGceFVpiAMyf2j2rvVthkg4o6adxY_E0-y_AJfnJdL1HhmWOBpFEUk6ziV1aFzSJIo-XpueJSFWpL7wrAsQ6shcLE3zQSZXJoXhdR7nr92-Y7SXgEE_a9kP_Q4uExJCWcaOcPkQ5Bgg=="
            }
        },
        {
            "name": "مثال خاطئ - توقيع محرف",
            "data": {
                "message": "wc_order_LI3SLQ7xA7IY9cib84907success23400",
                "signature_url_safe": "INVALID_SIGNATURE_HERE"
            }
        }
    ]
    
    print("🔐 اختبار التحقق من توقيع SofizPay")
    print("=" * 50)
    
    for i, example in enumerate(verification_examples, 1):
        print(f"\n📝 {example['name']} (#{i})")
        print("-" * 30)
        print(f"📄 الرسالة: {example['data']['message']}")
        print(f"🔑 التوقيع: {example['data']['signature_url_safe'][:50]}...")
        
        try:
            is_valid = client.verify_sofizpay_signature(example['data'])
            
            if is_valid:
                print("✅ التوقيع صحيح!")
            else:
                print("❌ التوقيع غير صحيح!")
                
        except Exception as e:
            print(f"⚠️ خطأ في التحقق: {e}")
        
        print("-" * 30)


def test_validation_errors():
    """اختبار أخطاء التحقق من البيانات"""
    print("\n🧪 اختبار أخطاء التحقق من البيانات")
    print("=" * 50)
    
    client = SofizPayClient()
    
    # اختبار بيانات ناقصة
    invalid_data_examples = [
        {
            "name": "بدون account",
            "data": {
                "amount": 100,
                "full_name": "أحمد محمد",
                "phone": "+213123456789",
                "email": "test@example.com"
            }
        },
        {
            "name": "مبلغ سالب",
            "data": {
                "account": "test_account",
                "amount": -50,
                "full_name": "أحمد محمد",
                "phone": "+213123456789",
                "email": "test@example.com"
            }
        },
        {
            "name": "بدون email",
            "data": {
                "account": "test_account",
                "amount": 100,
                "full_name": "أحمد محمد",
                "phone": "+213123456789"
            }
        }
    ]
    
    for example in invalid_data_examples:
        print(f"\n🔍 اختبار: {example['name']}")
        try:
            # هذا سيفشل مع ValidationError
            result = asyncio.run(client.make_cib_transaction(example['data']))
        except ValidationError as e:
            print(f"✅ تم اكتشاف الخطأ بنجاح: {e}")
        except Exception as e:
            print(f"⚠️ خطأ غير متوقع: {e}")


async def main():
    """الدالة الرئيسية لتشغيل الأمثلة"""
    print("🚀 أمثلة SofizPay SDK - CIB Transactions & Signature Verification")
    print("=" * 70)
    
    # مثال معاملة CIB
    print("\n📦 القسم 1: معاملات CIB")
    print("=" * 30)
    await cib_transaction_example()
    
    # مثال التحقق من التوقيع
    print("\n📦 القسم 2: التحقق من التوقيع")
    print("=" * 30)
    signature_verification_example()
    
    # اختبار أخطاء التحقق
    print("\n📦 القسم 3: اختبار التحقق من البيانات")
    print("=" * 30)
    test_validation_errors()
    
    print("\n✅ انتهت جميع الأمثلة!")


if __name__ == "__main__":
    print("💳 أمثلة SofizPay SDK - المعاملات والتوقيع")
    print("=" * 50)
    print("💡 نصيحة: تأكد من تحديث بيانات الحساب قبل التشغيل")
    print()
    
    # تشغيل الأمثلة
    asyncio.run(main())
