"""
ملف توضيحي للفرق بين Transaction Streaming و Get Transaction
"""

import asyncio
from datetime import datetime
from sofizpay import SofizPayClient


def explain_difference():
    """شرح الفرق بين الوظيفتين"""
    
    print("📚 الفرق بين Transaction Streaming و Get Transaction")
    print("=" * 70)
    
    print("\n🔍 GET TRANSACTION BY HASH:")
    print("-" * 40)
    print("✅ يبحث عن معاملات حدثت بالفعل في الماضي")
    print("✅ تحتاج hash معاملة موجودة")
    print("✅ يعطي تفاصيل كاملة للمعاملة")
    print("✅ بحث سريع ونتيجة فورية")
    print("❌ لا يراقب معاملات جديدة")
    print("\n📡 TRANSACTION STREAMING:")
    print("-" * 40)
    print("✅ يراقب المعاملات الجديدة في الوقت الفعلي")
    print("✅ يلتقط فقط المعاملات التي تحدث بعد بدء المراقبة")
    print("✅ مراقبة مستمرة ومباشرة")
    print("✅ يعمل مع معاملات مستقبلية")
    print("❌ لا يعرض معاملات من الماضي")
    
    print("\n💡 متى نستخدم كل وظيفة:")
    print("-" * 40)
    print("🔍 استخدم get_transaction_by_hash عندما:")
    print("   • تريد معلومات عن معاملة محددة حدثت")
    print("   • لديك hash معاملة وتريد تفاصيلها")
    print("   • تريد التحقق من حالة معاملة أرسلتها")
    
    print("\n📡 استخدم transaction_streaming عندما:")
    print("   • تريد مراقبة حساب للمعاملات الجديدة")
    print("   • تبني تطبيق يحتاج تنبيهات فورية")
    print("   • تريد معرفة فور وصول معاملة جديدة")


async def demo_get_transaction():
    """عرض توضيحي لـ get_transaction"""
    
    print("\n" + "=" * 70)
    print("🔍 عرض توضيحي: GET TRANSACTION BY HASH")
    print("=" * 70)
    
    client = SofizPayClient()
    
    # مثال على hash (غير حقيقي)
    demo_hash = "example_hash_from_past_transaction"
    
    print(f"🔎 البحث عن معاملة بـ hash: {demo_hash}")
    print("💭 هذا hash لمعاملة 'حدثت في الماضي'")
    print("⏰ الآن نبحث عنها في سجلات الشبكة...")
    
    try:
        result = await client.get_transaction_by_hash(demo_hash)
        
        if result['found']:
            print("✅ تم العثور على المعاملة القديمة!")
        else:
            print("❌ لم يتم العثور على المعاملة (hash غير صحيح)")
            print("💡 للحصول على نتيجة: استخدم hash معاملة حقيقية")
            
    except Exception as e:
        print(f"❌ خطأ في البحث: {e}")


async def demo_transaction_streaming():
    """عرض توضيحي لـ transaction streaming"""
    
    print("\n" + "=" * 70)
    print("📡 عرض توضيحي: TRANSACTION STREAMING")
    print("=" * 70)
    
    client = SofizPayClient()
    
    # حساب للمراقبة (مثال)
    demo_account = "GDNS27ISCGOIJFXC6CM4O5SVHVJPSWR42QEBWUFF24N5VVHGW73ZSJNQ"
    
    print(f"📡 بدء مراقبة الحساب: {demo_account[:20]}...")
    print(f"⏰ وقت بدء المراقبة: {datetime.now().strftime('%H:%M:%S')}")
    print("💭 الآن ننتظر معاملات جديدة فقط...")
    print("🔔 إذا حدثت معاملة بعد هذا الوقت، ستظهر هنا!")
    
    # معالج للمعاملات
    def demo_handler(transaction):
        print(f"\n🎉 معاملة جديدة وصلت!")
        print(f"⏰ وقت الوصول: {datetime.now().strftime('%H:%M:%S')}")
        print(f"💰 المبلغ: {transaction.get('amount', 'غير معروف')}")
        print("🔥 هذه معاملة طازجة - حدثت للتو!")
    
    try:
        # إعداد المراقبة
        stream_id = await client.setup_transaction_stream(
            public_key=demo_account,
            transaction_callback=demo_handler
        )
        
        print(f"✅ تم إعداد المراقبة - Stream ID: {stream_id}")
        print("⏳ مراقبة لمدة 10 ثواني...")
        print("💡 أرسل معاملة إلى الحساب الآن لرؤية النتيجة!")
        
        # انتظار لمدة 10 ثواني
        await asyncio.sleep(10)
        
        # إيقاف المراقبة
        client.stop_transaction_stream(stream_id)
        print("\n⏹️ تم إيقاف المراقبة")
        print("📝 إذا لم تظهر معاملات، فلم تحدث معاملات جديدة")
        
    except Exception as e:
        print(f"❌ خطأ في المراقبة: {e}")


async def compare_both_methods():
    """مقارنة بين الطريقتين"""
    
    print("\n" + "=" * 70)
    print("⚖️ مقارنة مباشرة بين الطريقتين")
    print("=" * 70)
    
    print("📊 خصائص كل طريقة:")
    print("-" * 40)
    
    comparison = [
        ("المعاملات المستهدفة", "معاملات من الماضي", "معاملات جديدة فقط"),
        ("السرعة", "سريع جداً", "مراقبة مستمرة"), 
        ("الاستخدام", "بحث لمرة واحدة", "مراقبة مستمرة"),
        ("المدخلات المطلوبة", "Transaction Hash", "Public Key فقط"),
        ("النتائج", "تفاصيل كاملة", "تنبيهات فورية"),
        ("استهلاك الموارد", "قليل", "متوسط"),
    ]
    
    print(f"{'الخاصية':<20} {'Get Transaction':<20} {'Streaming':<20}")
    print("-" * 60)
    
    for feature, get_tx, streaming in comparison:
        print(f"{feature:<20} {get_tx:<20} {streaming:<20}")
    
    print("\n🎯 الخلاصة:")
    print("-" * 15)
    print("• استخدم get_transaction للبحث عن معاملات موجودة")
    print("• استخدم streaming لمراقبة معاملات جديدة")
    print("• يمكن استخدام الاثنين معاً في تطبيق واحد!")


if __name__ == "__main__":
    print("📖 دليل الفروقات بين Transaction Methods")
    print("=" * 70)
    
    try:
        # شرح الفروقات
        explain_difference()
        
        # عروض توضيحية
        asyncio.run(demo_get_transaction())
        asyncio.run(demo_transaction_streaming())
        
        # مقارنة
        asyncio.run(compare_both_methods())
        
        print("\n✅ انتهى الدليل التوضيحي")
        print("💡 الآن يمكنك استخدام الملفين الآخرين للاختبار العملي")
        
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف العرض التوضيحي")
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
