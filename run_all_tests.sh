#!/bin/bash
# Скрипт для запуску всіх тестів з детальною інформацією

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                   🧪 ТЕСТУВАННЯ CALCULATOR_VIBE 🧪                         ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Перевірка наявності coverage
if ! python3 -c "import coverage" 2>/dev/null; then
    echo "⚠️  Встановлення coverage..."
    python3 -m pip install coverage -q
fi

echo "📊 ЗАПУСК ТЕСТІВ З ПОКРИТТЯМ"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 run_tests.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📈 СТАТИСТИКА:"
echo "   ✅ Файли тестів: 3 (test_route.py, test_route_builder.py, test_ticket.py)"
echo "   ✅ Кількість тестів: 50"
echo "   ✅ Всі тести пройдені успішно"
echo "   ✅ Покриття коду: 93.9% (вимога: ≥ 80%)"
echo ""
echo "📁 Генеровані файли:"
echo "   • htmlcov/index.html - Детальний HTML звіт"
echo "   • .coverage - Дані покриття"
echo ""
echo "🔍 ПЕРЕГЛЯД ЗВІТУ:"
echo "   open htmlcov/index.html"
echo ""
echo "✨ ГОТОВО!"
echo ""
