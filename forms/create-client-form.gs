/**
 * Creates the "طلب أتمتة لشركتك" client intake form in the Google account that runs it,
 * links it to a new Google Sheet for responses, and logs both links.
 *
 * How to use: paste into https://script.google.com (New project), save, choose
 * createClientForm, press Run, approve the permissions, then open View > Logs.
 */
function createClientForm() {
  var form = FormApp.create('طلب أتمتة لشركتك');
  form.setDescription(
    'أهلاً بحضرتك 😊\n' +
    'الفورم ده بياخد حوالي 5 دقايق، وبيساعدني أفهم شغلكم عشان أقترح أنسب حل أتمتة وأديك عرض سعر دقيق.\n' +
    'مفيش إجابة صح وإجابة غلط، ولو مش متأكد من حاجة اختار "مش متأكد" 👍'
  );
  form.setConfirmationMessage(
    'شكراً لحضرتك! ✅\n' +
    'هراجع إجاباتك وأتواصل معاك على الواتساب خلال 24 ساعة نحدد ميعاد مكالمة قصيرة.'
  );
  form.setProgressBar(true);
  form.setAllowResponseEdits(false);

  // 1. Contact details
  form.addSectionHeaderItem().setTitle('1. بيانات التواصل');
  form.addTextItem().setTitle('الاسم').setRequired(true);
  form.addTextItem().setTitle('اسم الشركة').setRequired(true);
  form.addListItem()
    .setTitle('مجال الشركة')
    .setChoiceValues(['متجر أونلاين', 'عقارات', 'عيادة أو مركز طبي', 'تعليم وكورسات',
      'مطاعم وكافيهات', 'خدمات', 'وكالة تسويق أو إعلانات', 'أخرى'])
    .setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('عدد الفريق')
    .setChoiceValues(['1 – 5', '6 – 20', '21 – 50', 'أكتر من 50']);
  form.addTextItem().setTitle('رقم الواتساب').setRequired(true);
  form.addTextItem().setTitle('الإيميل');

  // 2. The problem
  form.addPageBreakItem().setTitle('2. المشكلة اللي عاوز تحلها');
  form.addMultipleChoiceItem()
    .setTitle('أكتر مشكلة بتواجهك دلوقتي؟')
    .setChoiceValues([
      'الـ Leads كتير ومحدش بيلحق يرد',
      'رسائل ودعم كتير والفريق مش ملاحق',
      'شغل إداري يدوي بياكل وقت الفريق',
      'التقارير والمحتوى بياخدوا وقت'
    ])
    .showOtherOption(true)
    .setRequired(true);
  form.addParagraphTextItem()
    .setTitle('إيه المهمة اللي بتتكرر وعاوزها تتعمل لوحدها؟')
    .setHelpText('اكتبها زي ما بتحصل دلوقتي خطوة بخطوة. مثال: العميل يبعت رسالة ← حد من الفريق يرد ← يسجل بياناته في شيت')
    .setRequired(true);
  form.addCheckboxItem()
    .setTitle('المهمة دي بتبدأ إزاي؟')
    .setChoiceValues(['رسالة واتساب', 'رسالة فيسبوك أو إنستجرام', 'فورم على الموقع',
      'إعلان (Lead Form)', 'إيميل', 'أوردر جديد', 'ميعاد ثابت (كل يوم أو أسبوع)'])
    .showOtherOption(true)
    .setRequired(true);
  form.addParagraphTextItem()
    .setTitle('في الآخر عاوز يحصل إيه؟')
    .setHelpText('مثال: العميل ياخد رد فوري، وبياناته تتسجل، وفريق المبيعات يوصله تنبيه')
    .setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('المهمة بتحصل كام مرة تقريباً في اليوم؟')
    .setChoiceValues(['أقل من 10', '10 – 50', '50 – 200', 'أكتر من 200', 'مش متأكد'])
    .setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('بتاخد من وقت فريقك قد إيه دلوقتي؟')
    .setChoiceValues(['أقل من ساعة يومياً', '1 – 3 ساعات يومياً', 'أكتر من 3 ساعات يومياً', 'مش متأكد']);

  // 3. Tools
  form.addPageBreakItem().setTitle('3. الأدوات اللي بتستخدموها');
  form.addCheckboxItem()
    .setTitle('بتستخدموا أنهي أدوات؟')
    .setChoiceValues(['واتساب بيزنس', 'فيسبوك وإنستجرام', 'Google Sheets', 'Excel', 'Gmail',
      'Outlook', 'CRM (زي HubSpot أو Zoho)', 'متجر إلكتروني (Shopify أو WooCommerce أو غيرهم)',
      'برنامج حسابات', 'Google Calendar أو برنامج حجز مواعيد'])
    .showOtherOption(true)
    .setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('عندكم اشتراك في WhatsApp Business API؟')
    .setChoiceValues(['آه', 'لأ', 'مش عارف']);
  form.addMultipleChoiceItem()
    .setTitle('عندكم سيرفر أو اشتراك n8n؟')
    .setChoiceValues(['آه', 'لأ', 'مش عارف']);

  // 4. AI and human control
  form.addPageBreakItem().setTitle('4. الذكاء الاصطناعي والتحكم');
  form.addCheckboxItem()
    .setTitle('محتاج الذكاء الاصطناعي يعمل إيه؟')
    .setChoiceValues(['يرد على العملاء', 'يحجز مواعيد', 'يفهم ويصنّف الرسايل أو الإيميلات',
      'يقيّم العملاء المحتملين', 'يطلّع بيانات من نصوص أو صور أو فواتير',
      'يكتب تقارير أو ملخصات أو محتوى', 'مش محتاج', 'مش متأكد'])
    .setRequired(true);
  form.addParagraphTextItem()
    .setTitle('فيه خطوة لازم موظف يراجعها أو يوافق عليها قبل ما تكمل؟')
    .setHelpText('مثال: الخصومات لازم المدير يوافق عليها، أو الشكاوى توصل لمسؤول خدمة العملاء');

  // 5. Services, timing and budget
  form.addPageBreakItem().setTitle('5. الميعاد والميزانية');
  form.addCheckboxItem()
    .setTitle('لو شفت المنيو، أنهي خدمة لفتت نظرك؟')
    .setChoiceValues(['Lead Radar', 'Speed-to-Lead', 'Lead Router', 'Luna (WhatsApp AI Agent)',
      'Support Compass', 'Appointment Guard', 'Review Booster', 'Order Flow', 'Invoice Reader',
      'Monday Brief', 'Content Pilot', 'Welcome Engine', 'Team Onboarding', 'Team Brain',
      'مش متأكد / لسه مشفتش المنيو']);
  form.addMultipleChoiceItem()
    .setTitle('محتاجه إمتى؟')
    .setChoiceValues(['في أسرع وقت', 'خلال شهر', 'خلال 1 – 3 شهور', 'لسه بستكشف'])
    .setRequired(true);
  form.addTextItem().setTitle('لو عندك ميزانية تقريبية اكتبها');
  form.addMultipleChoiceItem()
    .setTitle('تحب نكلمك إمتى؟')
    .setChoiceValues(['الصبح', 'بعد الضهر', 'بالليل']);
  form.addParagraphTextItem().setTitle('أي ملاحظات تانية؟');

  // Responses sheet
  var sheet = SpreadsheetApp.create('ردود فورم طلب الأتمتة');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId());

  Logger.log('لينك الفورم للعملاء: ' + form.getPublishedUrl());
  Logger.log('لينك تعديل الفورم: ' + form.getEditUrl());
  Logger.log('شيت الردود: ' + sheet.getUrl());
}
