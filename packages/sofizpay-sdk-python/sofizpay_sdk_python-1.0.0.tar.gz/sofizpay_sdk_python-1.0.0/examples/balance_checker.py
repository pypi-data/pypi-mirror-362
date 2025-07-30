"""
مثال لفحص أرصدة الحسابات باستخدام SofizPay SDK
"""

import asyncio
from sofizpay import SofizPayClient, ValidationError, NetworkError


async def check_dzt_balance(client: SofizPayClient, public_key: str):
    """فحص رصيد DZT لحساب معين"""
    try:
        print(f"🔍 فحص رصيد DZT للحساب...")
        print(f"🔑 {public_key}")
        
        balance = await client.get_dzt_balance(public_key)
        
        print(f"💰 رصيد DZT: {balance:,.2f} DZT")
        
        if balance == 0:
            print("⚠️ الحساب لا يحتوي على رصيد DZT")
        elif balance < 1:
            print("🟡 رصيد منخفض")
        elif balance < 100:
            print("🟢 رصيد متوسط")
        else:
            print("🟢 رصيد جيد")
            
        return balance
        
    except ValidationError as e:
        print(f"❌ خطأ في التحقق: {e}")
        return None
    except NetworkError as e:
        print(f"❌ خطأ في الشبكة: {e}")
        return None
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        return None


async def check_all_balances(client: SofizPayClient, public_key: str):
    """فحص جميع الأرصدة لحساب معين"""
    try:
        print(f"\n📊 فحص جميع الأرصدة للحساب...")
        print(f"🔑 {public_key}")
        print("-" * 50)
        
        balances = await client.get_account_balances(public_key)
        
        if not balances:
            print("⚠️ لم يتم العثور على أرصدة للحساب")
            return
            
        print(f"📈 إجمالي الأصول: {len(balances)}")
        print()
        
        for i, balance in enumerate(balances, 1):
            print(f"الأصل #{i}:")
            
            if balance.get('asset_type') == 'native':
                print(f"  💎 النوع: XLM (Stellar Lumens)")
                print(f"  💰 الرصيد: {float(balance['balance']):,.7f} XLM")
            else:
                asset_code = balance.get('asset_code', 'غير معروف')
                asset_issuer = balance.get('asset_issuer', 'غير معروف')
                balance_amount = float(balance.get('balance', 0))
                
                print(f"  🏷️ رمز الأصل: {asset_code}")
                print(f"  💰 الرصيد: {balance_amount:,.7f} {asset_code}")
                print(f"  🏦 المُصدر: {asset_issuer[:10]}...{asset_issuer[-10:]}")
                
                # تمييز خاص لـ DZT
                if asset_code == 'DZT':
                    print(f"  ⭐ هذا هو رصيد SofizPay DZT!")
            
            # إضافة معلومات إضافية إذا توفرت
            if 'limit' in balance:
                print(f"  📏 الحد الأقصى: {balance['limit']}")
            if 'buying_liabilities' in balance:
                print(f"  📉 التزامات الشراء: {balance['buying_liabilities']}")
            if 'selling_liabilities' in balance:
                print(f"  📈 التزامات البيع: {balance['selling_liabilities']}")
                
            print()
            
    except Exception as e:
        print(f"❌ خطأ في فحص الأرصدة: {e}")


async def validate_account(client: SofizPayClient, public_key: str):
    """التحقق من صحة الحساب"""
    print(f"🔍 التحقق من صحة الحساب...")
    
    if not client.validate_public_key(public_key):
        print("❌ المفتاح العام غير صالح!")
        return False
        
    print("✅ المفتاح العام صالح")
    return True


async def main():
    # قائمة الحسابات للفحص (يجب استبدالها بالقيم الفعلية)
    accounts_to_check = [
        "GDNS27ISCGOIJFXC6CM4O5SVHVJPSWR42QEBWUFF24N5VVHGW73ZSJNQ",
        "GDNS27ISCGOIJFXC6CM4O5SVHVJPSWR42QEBWUFF24N5VVHGW73ZSJNQ",
        # يمكن إضافة المزيد من الحسابات
    ]
    
    # إنشاء عميل SofizPay
    client = SofizPayClient()
    
    print("💳 فاحص أرصدة SofizPay")
    print("=" * 50)
    
    for i, public_key in enumerate(accounts_to_check, 1):
        if not public_key or public_key == "PUBLIC_KEY_1_HERE":
            print(f"⚠️ يرجى تحديث الحساب #{i} بمفتاح عام صالح")
            continue
            
        print(f"\n📋 فحص الحساب #{i}")
        print("=" * 30)
        
        # التحقق من صحة الحساب
        if not await validate_account(client, public_key):
            continue
            
        # فحص رصيد DZT
        await check_dzt_balance(client, public_key)
        
        # فحص جميع الأرصدة
        await check_all_balances(client, public_key)
        
        print("-" * 50)


if __name__ == "__main__":
    # تشغيل فاحص الأرصدة
    asyncio.run(main())
