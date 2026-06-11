from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.assets.models import Angle, Creative, Hook
from apps.chatbot.models import ChatMessage, ChatSession
from apps.finance.models import Expense, Revenue
from apps.pipeline.models import Campaign, Product
from apps.prediction.models import PredictionLog


class Command(BaseCommand):
    help = 'Seed a polished demo workspace for the CRM presentation.'

    def handle(self, *args, **options):
        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if not user.has_usable_password():
            user.set_password('admin')
            user.save(update_fields=['password'])

        today = timezone.localdate()

        angles = self.create_angles()
        products = self.create_products(user)
        campaigns = self.create_campaigns(products, today)
        self.create_assets(angles, campaigns)
        self.create_finance(campaigns, today)
        self.create_predictions(user, today)
        self.create_chat(user)

        self.stdout.write(self.style.SUCCESS(
            'Demo data ready: '
            f'{Product.objects.count()} products, '
            f'{Campaign.objects.count()} campaigns, '
            f'{Creative.objects.count()} creatives, '
            f'{Hook.objects.count()} hooks.'
        ))

    def create_angles(self):
        data = [
            ('Morning Routine Reset', Angle.Category.PROBLEM_SOLUTION, 76.4),
            ('Save Time With Automation', Angle.Category.BENEFIT, 81.2),
            ('Limited Launch Bundle', Angle.Category.OFFER, 69.8),
            ('Before/After Transformation', Angle.Category.BENEFIT, 88.1),
            ('Founder Story Trust Builder', Angle.Category.PROBLEM_SOLUTION, 72.6),
        ]
        angles = {}
        for name, category, rate in data:
            angle, _ = Angle.objects.update_or_create(
                name=name,
                defaults={'category': category, 'success_rate': rate},
            )
            angles[name] = angle
        return angles

    def create_products(self, user):
        data = [
            {
                'name': 'GlowLift LED Face Mask',
                'description': 'At-home skincare device positioned for busy professionals who want visible routines without clinic visits.',
                'status': Product.Status.ACTIVE,
                'score': 87,
                'notes': 'Best audience: women 25-44, skincare buyers, high AOV bundles. Demo angle works well with UGC before/after clips.',
            },
            {
                'name': 'FocusFlow Desk Lamp',
                'description': 'Smart desk lamp with timer modes, warm/cool light presets, and productivity positioning for remote workers.',
                'status': Product.Status.PLANNING,
                'score': 73,
                'notes': 'Needs stronger hook around eye comfort and deep-work rituals. Test against productivity and home-office audiences.',
            },
            {
                'name': 'HydroPulse Bottle',
                'description': 'Hydration bottle with reminder glow, infuser core, and fitness/lifestyle positioning.',
                'status': Product.Status.ACTIVE,
                'score': 79,
                'notes': 'Bundle with replacement filters. Strong short-form hook: "I forgot water until this bottle reminded me."',
            },
            {
                'name': 'MiniBlend Portable Mixer',
                'description': 'USB-C portable blender for protein shakes, smoothies, and office snacks.',
                'status': Product.Status.EVALUATED,
                'score': 91,
                'notes': 'Validated winner. Scale with creator videos, recipe carousel ads, and gym partnership landing page.',
            },
            {
                'name': 'PetCalm Smart Feeder',
                'description': 'App-connected feeder for scheduled meals, travel peace of mind, and pet-owner retention campaigns.',
                'status': Product.Status.PLANNING,
                'score': 68,
                'notes': 'Position around peace of mind instead of tech features. Needs pricing test against standard feeders.',
            },
            {
                'name': 'PosturePro Seat Cushion',
                'description': 'Ergonomic cushion for office chairs, car seats, and long study sessions.',
                'status': Product.Status.EVALUATED,
                'score': 84,
                'notes': 'Reliable evergreen product. Retarget with pain-point testimonials and bundle discount.',
            },
        ]
        products = {}
        for item in data:
            product, _ = Product.objects.update_or_create(
                name=item['name'],
                defaults={
                    'description': item['description'],
                    'status': item['status'],
                    'score': item['score'],
                    'notes': item['notes'],
                    'owner': user,
                },
            )
            products[item['name']] = product
        return products

    def create_campaigns(self, products, today):
        data = [
            ('GlowLift LED Face Mask', 'TikTok UGC Launch', -24, 12000, Campaign.Status.RUNNING),
            ('GlowLift LED Face Mask', 'Retargeting Bundle Push', -8, 5500, Campaign.Status.RUNNING),
            ('FocusFlow Desk Lamp', 'Remote Work Validation', 4, 3000, Campaign.Status.DRAFT),
            ('HydroPulse Bottle', 'Fitness Creator Sprint', -18, 7200, Campaign.Status.RUNNING),
            ('MiniBlend Portable Mixer', 'Summer Recipe Scale', -45, 15000, Campaign.Status.DONE),
            ('PetCalm Smart Feeder', 'Peace of Mind Test', 2, 4200, Campaign.Status.DRAFT),
            ('PosturePro Seat Cushion', 'Back-to-Office Evergreen', -60, 9800, Campaign.Status.DONE),
        ]
        campaigns = {}
        for product_name, campaign_name, start_offset, budget, status in data:
            campaign, _ = Campaign.objects.update_or_create(
                product=products[product_name],
                name=campaign_name,
                defaults={
                    'start_date': today + timedelta(days=start_offset),
                    'end_date': None if status != Campaign.Status.DONE else today + timedelta(days=start_offset + 21),
                    'budget': Decimal(str(budget)),
                    'status': status,
                },
            )
            campaigns[campaign_name] = campaign
        return campaigns

    def create_assets(self, angles, campaigns):
        creatives = [
            ('GlowLift 15-sec Bathroom Mirror UGC', 'TikTok UGC Launch', 'Before/After Transformation', Creative.MediaType.VIDEO, True),
            ('Dermatologist Style Static Comparison', 'TikTok UGC Launch', 'Founder Story Trust Builder', Creative.MediaType.IMAGE, False),
            ('Bundle Offer Carousel', 'Retargeting Bundle Push', 'Limited Launch Bundle', Creative.MediaType.IMAGE, True),
            ('Desk Setup Deep Work Reel', 'Remote Work Validation', 'Save Time With Automation', Creative.MediaType.VIDEO, False),
            ('Gym Bag Smoothie Demo', 'Summer Recipe Scale', 'Before/After Transformation', Creative.MediaType.VIDEO, True),
            ('Hydration Reminder Lifestyle Ad', 'Fitness Creator Sprint', 'Morning Routine Reset', Creative.MediaType.VIDEO, True),
            ('Pet Owner Travel Weekend Static', 'Peace of Mind Test', 'Founder Story Trust Builder', Creative.MediaType.IMAGE, False),
            ('Office Chair Pain Point Testimonial', 'Back-to-Office Evergreen', 'Morning Routine Reset', Creative.MediaType.VIDEO, True),
        ]
        for title, campaign_name, angle_name, media_type, is_winner in creatives:
            Creative.objects.update_or_create(
                title=title,
                defaults={
                    'campaign': campaigns[campaign_name],
                    'angle': angles[angle_name],
                    'media_type': media_type,
                    'is_winner': is_winner,
                },
            )

        hooks = [
            ('Your skincare routine is missing the 10 minutes that do the heavy lifting.', Hook.Platform.SOCIAL, Hook.Trigger.CURIOSITY, 'Before/After Transformation', 88),
            ('Stop guessing when to drink water during your workouts.', Hook.Platform.SOCIAL, Hook.Trigger.PAIN, 'Morning Routine Reset', 79),
            ('This tiny blender made my 7am protein shake actually happen.', Hook.Platform.SOCIAL, Hook.Trigger.DEMO, 'Before/After Transformation', 91),
            ('Your desk light should match your focus, not fight it.', Hook.Platform.SEARCH, Hook.Trigger.PAIN, 'Save Time With Automation', 74),
            ('A calmer way to feed your pet while you are away for the weekend.', Hook.Platform.DISPLAY, Hook.Trigger.PAIN, 'Founder Story Trust Builder', 71),
            ('Back pain after two hours at a desk? Start with the chair, not your calendar.', Hook.Platform.SEARCH, Hook.Trigger.PAIN, 'Morning Routine Reset', 83),
            ('Launch bundle: mask, serum guide, and travel pouch before the price changes.', Hook.Platform.SOCIAL, Hook.Trigger.CURIOSITY, 'Limited Launch Bundle', 69),
        ]
        for text, platform, trigger, angle_name, score in hooks:
            Hook.objects.update_or_create(
                text=text,
                defaults={
                    'platform': platform,
                    'trigger_type': trigger,
                    'angle': angles[angle_name],
                    'performance_score': score,
                },
            )

    def create_finance(self, campaigns, today):
        finance = {
            'TikTok UGC Launch': {
                'expenses': [(4200, Expense.Category.ADS, -20), (1800, Expense.Category.PRODUCTION, -22), (950, Expense.Category.TOOLS, -10)],
                'revenues': [(11200, 'Shopify checkout', -14), (8450, 'Retargeting sales', -5)],
            },
            'Retargeting Bundle Push': {
                'expenses': [(2400, Expense.Category.ADS, -7), (600, Expense.Category.PRODUCTION, -6)],
                'revenues': [(9100, 'Bundle orders', -2)],
            },
            'Remote Work Validation': {
                'expenses': [(700, Expense.Category.PRODUCTION, -1)],
                'revenues': [],
            },
            'Fitness Creator Sprint': {
                'expenses': [(3100, Expense.Category.ADS, -16), (1250, Expense.Category.PRODUCTION, -18)],
                'revenues': [(10200, 'Creator code sales', -9), (3900, 'Email follow-up', -3)],
            },
            'Summer Recipe Scale': {
                'expenses': [(6800, Expense.Category.ADS, -42), (2200, Expense.Category.PRODUCTION, -43), (900, Expense.Category.TOOLS, -30)],
                'revenues': [(24200, 'Paid social', -34), (17800, 'Influencer links', -24), (6500, 'Email upsell', -18)],
            },
            'Peace of Mind Test': {
                'expenses': [(500, Expense.Category.PRODUCTION, -1)],
                'revenues': [],
            },
            'Back-to-Office Evergreen': {
                'expenses': [(4200, Expense.Category.ADS, -55), (1100, Expense.Category.PRODUCTION, -57), (400, Expense.Category.OTHER, -44)],
                'revenues': [(13200, 'Search ads', -48), (7400, 'Remarketing', -38), (3100, 'Amazon referral', -25)],
            },
        }
        for campaign_name, rows in finance.items():
            campaign = campaigns[campaign_name]
            for amount, category, day_offset in rows['expenses']:
                Expense.objects.update_or_create(
                    campaign=campaign,
                    amount=Decimal(str(amount)),
                    category=category,
                    date=today + timedelta(days=day_offset),
                    defaults={},
                )
            for amount, source, day_offset in rows['revenues']:
                Revenue.objects.update_or_create(
                    campaign=campaign,
                    amount=Decimal(str(amount)),
                    source=source,
                    date=today + timedelta(days=day_offset),
                    defaults={},
                )

    def create_predictions(self, user, today):
        rows = [
            ({'category': 'beauty', 'price': 89.0, 'competition_level': 'medium', 'angle_type': 'benefit', 'initial_ctr': 0.041}, 'High', 0.87, -1),
            ({'category': 'tech', 'price': 49.0, 'competition_level': 'high', 'angle_type': 'problem_solution', 'initial_ctr': 0.025}, 'Medium', 0.66, -2),
            ({'category': 'fitness', 'price': 34.9, 'competition_level': 'medium', 'angle_type': 'offer', 'initial_ctr': 0.037}, 'High', 0.82, -3),
            ({'category': 'home', 'price': 59.0, 'competition_level': 'low', 'angle_type': 'benefit', 'initial_ctr': 0.031}, 'Medium', 0.71, -4),
            ({'category': 'food', 'price': 24.0, 'competition_level': 'high', 'angle_type': 'offer', 'initial_ctr': 0.018}, 'Low', 0.58, -5),
        ]
        for features, predicted_class, confidence, day_offset in rows:
            PredictionLog.objects.update_or_create(
                user=user,
                input_features=features,
                defaults={
                    'predicted_class': predicted_class,
                    'confidence': confidence,
                    'created_at': today + timedelta(days=day_offset),
                },
            )

    def create_chat(self, user):
        session = ChatSession.objects.filter(user=user).order_by('id').first()
        if session is None:
            session = ChatSession.objects.create(user=user)

        messages = [
            (ChatMessage.Role.USER, 'Which campaign should I show first in tomorrow presentation?'),
            (ChatMessage.Role.ASSISTANT, 'Start with MiniBlend because it has strong ROI, then compare it with GlowLift to show the CRM can track both scaling and active launch work.'),
            (ChatMessage.Role.USER, 'What should I improve before scaling HydroPulse?'),
            (ChatMessage.Role.ASSISTANT, 'The creator sprint is profitable, so test a second hook around hydration reminders and keep the bundle offer ready for retargeting.'),
        ]
        existing = set(ChatMessage.objects.filter(session=session).values_list('content', flat=True))
        for role, content in messages:
            if content not in existing:
                ChatMessage.objects.create(session=session, role=role, content=content)
