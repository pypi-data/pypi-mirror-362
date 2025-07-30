"""
مثال أساسي لإرسال دفعة DZT باستخدام SofizPay SDK
"""

import asyncio
from sofizpay import SofizPayClient, PaymentError, ValidationError


async def main():
    # إنشاء عميل SofizPay
    client = SofizPayClient()
    
    # معلومات المعاملة (يجب استبدالها بالقيم الفعلية)
    source_secret = "SBKNMEIHTHOVSVV7GLWDPC5DACK7GO3CDUABKMKFYBJA4TARLLFT7EC4"  # المفتاح السري للحساب المرسل
    destination_public_key = "GB6MXBJGI4A7DJKBKUUTMLEUPPG3YWH2IBZQUHXZQJPLUVJOTAKCRDVC"  # المفتاح العام للحساب المستقبل
    amount = "1"  # المبلغ بالـ DZT
    memo = "SofizPay Test Payment"  # Keep memo short for Stellar limit
    
    try:
        print("🚀 بدء إرسال الدفعة...")
        print(f"المبلغ: {amount} DZT")
        print(f"إلى: {destination_public_key}")
        print(f"المذكرة: {memo}")
        print("-" * 50)
        
        # إرسال الدفعة
        result = await client.send_payment(
            source_secret=source_secret,
            destination_public_key=destination_public_key,
            amount=amount,
            memo=memo
        )
        
        if result['success']:
            print("✅ تم إرسال الدفعة بنجاح!")
            print(f"🔗 Hash المعاملة: {result['hash']}")
            print(f"⏱️ المدة: {result['duration']:.2f} ثانية")
            
            if 'ledger' in result:
                print(f"📊 رقم Ledger: {result['ledger']}")
                
        else:
            print("❌ فشل في إرسال الدفعة!")
            print(f"🚫 الخطأ: {result['error']}")
            print(f"⏱️ المدة: {result['duration']:.2f} ثانية")
            
    except ValidationError as e:
        print(f"❌ خطأ في التحقق من البيانات: {e}")
    except PaymentError as e:
        print(f"❌ خطأ في الدفع: {e}")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")


if __name__ == "__main__":
    print("🏦 مثال إرسال دفعة SofizPay")
    print("=" * 50)
    
    # تشغيل المثال
    asyncio.run(main())
