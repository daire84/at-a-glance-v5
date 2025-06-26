# 09 - Testing and Validation: Quality Assurance Strategy

## 🧪 Testing Overview

The Movie Magic Stripboard integration requires comprehensive testing across multiple dimensions: functionality, performance, user experience, and industry compatibility. This document outlines the complete testing strategy to ensure professional-grade quality.

---

## 🎯 Testing Philosophy

### **Core Principles**
1. **User-Centric Testing**: Test real production workflows
2. **Performance-First**: Every test includes performance validation
3. **Industry Standards**: Validate against professional expectations
4. **Cross-Platform Consistency**: Ensure identical experience across devices
5. **Regression Prevention**: Protect existing functionality

### **Quality Gates**
- **No feature ships without 95% test coverage**
- **All user workflows must pass E2E tests**
- **Performance benchmarks must be met**
- **Professional user validation required**
- **Security review mandatory**

---

## 🔧 Unit Testing Strategy

### **Data Model Testing**

#### Scene Management Tests
```python
# tests/test_scene_models.py
class TestSceneModel(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Film")
        self.calendar_day = CalendarDay.objects.create(
            project=self.project, 
            date="2024-03-15"
        )
    
    def test_scene_creation(self):
        """Test basic scene creation and validation"""
        scene = Scene.objects.create(
            calendar_day=self.calendar_day,
            scene_number="1A",
            description="INT. OFFICE - DAY",
            estimated_duration=120,
            scene_order=1
        )
        
        self.assertEqual(scene.scene_number, "1A")
        self.assertEqual(scene.calendar_day, self.calendar_day)
        self.assertTrue(scene.created_at)
    
    def test_scene_ordering_constraints(self):
        """Test scene ordering within calendar days"""
        # Create multiple scenes
        scene1 = Scene.objects.create(
            calendar_day=self.calendar_day,
            scene_number="1",
            scene_order=1
        )
        scene2 = Scene.objects.create(
            calendar_day=self.calendar_day,
            scene_number="2", 
            scene_order=2
        )
        
        # Test ordering retrieval
        ordered_scenes = Scene.objects.filter(
            calendar_day=self.calendar_day
        ).order_by('scene_order')
        
        self.assertEqual(list(ordered_scenes), [scene1, scene2])
    
    def test_scene_cascade_deletion(self):
        """Test proper cleanup when calendar day is deleted"""
        scene = Scene.objects.create(
            calendar_day=self.calendar_day,
            scene_number="1"
        )
        
        self.calendar_day.delete()
        
        # Scene should be deleted too
        self.assertFalse(Scene.objects.filter(id=scene.id).exists())
```

#### Resource Management Tests
```python
# tests/test_resource_models.py
class TestResourceManagement(TestCase):
    def test_cast_assignment(self):
        """Test cast member assignment to scenes"""
        actor = CastMember.objects.create(
            name="John Actor",
            role="Lead"
        )
        scene = self.create_test_scene()
        
        scene.cast_members.add(actor)
        
        self.assertIn(actor, scene.cast_members.all())
    
    def test_equipment_requirements(self):
        """Test equipment requirement tracking"""
        camera = Equipment.objects.create(
            name="RED Camera",
            category="camera"
        )
        scene = self.create_test_scene()
        
        requirement = EquipmentRequirement.objects.create(
            scene=scene,
            equipment=camera,
            quantity=1,
            notes="Primary camera"
        )
        
        self.assertEqual(requirement.quantity, 1)
        self.assertEqual(requirement.equipment, camera)
```

### **API Endpoint Testing**

#### Scene CRUD Operations
```python
# tests/test_scene_api.py
class TestSceneAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com')
        self.client.force_authenticate(user=self.user)
        self.project = self.create_test_project()
        self.calendar_day = self.create_test_calendar_day()
    
    def test_scene_creation_api(self):
        """Test scene creation via API"""
        data = {
            'calendar_day': self.calendar_day.id,
            'scene_number': '1A',
            'description': 'INT. OFFICE - DAY',
            'estimated_duration': 120
        }
        
        response = self.client.post('/api/scenes/', data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['scene_number'], '1A')
        self.assertTrue(Scene.objects.filter(scene_number='1A').exists())
    
    def test_scene_reordering_api(self):
        """Test scene reordering via drag-and-drop API"""
        # Create multiple scenes
        scenes = [
            self.create_test_scene(scene_number=f"{i}", scene_order=i)
            for i in range(1, 4)
        ]
        
        # Reorder: move scene 3 to position 1
        data = {
            'scene_id': scenes[2].id,
            'new_order': 1,
            'calendar_day_id': self.calendar_day.id
        }
        
        response = self.client.post('/api/scenes/reorder/', data)
        
        self.assertEqual(response.status_code, 200)
        
        # Verify new order
        updated_scenes = Scene.objects.filter(
            calendar_day=self.calendar_day
        ).order_by('scene_order')
        
        self.assertEqual(updated_scenes[0].id, scenes[2].id)
```

### **Service Layer Testing**

#### Schedule Generation Tests
```python
# tests/test_schedule_services.py
class TestScheduleGeneration(TestCase):
    def test_one_liner_generation(self):
        """Test one-liner schedule generation"""
        # Create test data
        project = self.create_test_project()
        scenes = self.create_test_scenes(project, count=5)
        
        generator = ScheduleGenerator()
        one_liner = generator.generate_one_liner(project.id)
        
        self.assertIsInstance(one_liner, dict)
        self.assertIn('scenes', one_liner)
        self.assertEqual(len(one_liner['scenes']), 5)
        
        # Verify scene order preservation
        scene_numbers = [s['scene_number'] for s in one_liner['scenes']]
        expected_order = ['1', '2', '3', '4', '5']
        self.assertEqual(scene_numbers, expected_order)
    
    def test_conflict_detection(self):
        """Test resource conflict detection"""
        # Create conflicting schedules
        actor = self.create_test_actor()
        day1 = self.create_calendar_day(date='2024-03-15')
        day2 = self.create_calendar_day(date='2024-03-15')  # Same day, different project
        
        # Assign same actor to both days
        scene1 = self.create_test_scene(calendar_day=day1)
        scene2 = self.create_test_scene(calendar_day=day2)
        scene1.cast_members.add(actor)
        scene2.cast_members.add(actor)
        
        detector = ConflictDetector()
        conflicts = detector.detect_cast_conflicts(date='2024-03-15')
        
        self.assertTrue(len(conflicts) > 0)
        self.assertIn('cast_conflicts', conflicts)
```

---

## 🌐 Integration Testing

### **Full Workflow Integration Tests**

#### Calendar + Scene Integration
```python
# tests/test_calendar_scene_integration.py
class TestCalendarSceneIntegration(TestCase):
    def test_calendar_scene_expansion(self):
        """Test expanding calendar day to show scenes"""
        project = self.create_test_project()
        calendar_day = self.create_calendar_day(project=project)
        scenes = [
            self.create_test_scene(calendar_day=calendar_day, scene_number=f"{i}")
            for i in range(1, 4)
        ]
        
        # Test calendar API with scene expansion
        response = self.client.get(
            f'/api/calendar/{project.id}/?include_scenes=true'
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify scenes are included
        calendar_data = response.json()
        day_data = next(
            day for day in calendar_data['days'] 
            if day['date'] == str(calendar_day.date)
        )
        
        self.assertIn('scenes', day_data)
        self.assertEqual(len(day_data['scenes']), 3)
    
    def test_scene_summary_calculation(self):
        """Test automatic scene summary calculation"""
        calendar_day = self.create_calendar_day()
        
        # Create scenes with different durations
        scenes = [
            self.create_test_scene(
                calendar_day=calendar_day,
                estimated_duration=60
            ),
            self.create_test_scene(
                calendar_day=calendar_day,
                estimated_duration=90
            )
        ]
        
        # Test summary API
        response = self.client.get(
            f'/api/calendar-days/{calendar_day.id}/summary/'
        )
        
        summary = response.json()
        self.assertEqual(summary['total_duration'], 150)
        self.assertEqual(summary['scene_count'], 2)
```

### **Database Integration Tests**

#### Transaction Integrity Tests
```python
# tests/test_database_integrity.py
class TestDatabaseIntegrity(TestCase):
    def test_scene_reordering_transaction(self):
        """Test that scene reordering is atomic"""
        calendar_day = self.create_calendar_day()
        scenes = [
            self.create_test_scene(calendar_day=calendar_day, scene_order=i)
            for i in range(1, 4)
        ]
        
        with mock.patch('django.db.transaction.atomic') as mock_atomic:
            # Simulate transaction failure
            mock_atomic.side_effect = Exception("Database error")
            
            with self.assertRaises(Exception):
                reorder_scenes(calendar_day.id, [3, 1, 2])
            
            # Verify original order is preserved
            current_scenes = Scene.objects.filter(
                calendar_day=calendar_day
            ).order_by('scene_order')
            
            original_order = [s.scene_order for s in current_scenes]
            self.assertEqual(original_order, [1, 2, 3])
```

---

## 🖥️ End-to-End Testing

### **User Workflow E2E Tests**

#### Complete Scene Management Workflow
```javascript
// tests/e2e/scene-management.spec.js
const { test, expect } = require('@playwright/test');

test.describe('Scene Management Workflow', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/login');
        await page.fill('[data-testid="email"]', 'test@strips.com');
        await page.fill('[data-testid="password"]', 'testpass');
        await page.click('[data-testid="login-button"]');
        
        // Navigate to test project
        await page.goto('/projects/test-project/calendar');
    });
    
    test('should create and manage scenes', async ({ page }) => {
        // Expand a calendar day
        await page.click('[data-testid="expand-day-2024-03-15"]');
        
        // Verify expansion animation completes
        await expect(page.locator('.scene-list')).toBeVisible({ timeout: 5000 });
        
        // Add new scene
        await page.click('[data-testid="add-scene-button"]');
        await page.fill('[data-testid="scene-number"]', '1A');
        await page.fill('[data-testid="scene-description"]', 'INT. OFFICE - DAY');
        await page.fill('[data-testid="estimated-duration"]', '120');
        await page.click('[data-testid="save-scene"]');
        
        // Verify scene appears in list
        await expect(page.locator('[data-testid="scene-1A"]')).toBeVisible();
        
        // Test scene reordering
        await page.dragAndDrop(
            '[data-testid="scene-1A"]',
            '[data-testid="scene-drop-zone-2"]'
        );
        
        // Verify reorder completed
        const sceneOrder = await page.locator('.scene-item').allTextContents();
        expect(sceneOrder[1]).toContain('1A');
    });
    
    test('should handle cast assignment', async ({ page }) => {
        await page.click('[data-testid="expand-day-2024-03-15"]');
        await page.click('[data-testid="scene-1A"]');
        
        // Open cast assignment
        await page.click('[data-testid="assign-cast"]');
        
        // Search and select cast member
        await page.fill('[data-testid="cast-search"]', 'John Actor');
        await page.click('[data-testid="cast-option-john-actor"]');
        await page.click('[data-testid="add-cast-member"]');
        
        // Verify cast member appears
        await expect(page.locator('[data-testid="cast-john-actor"]')).toBeVisible();
    });
});
```

### **Performance E2E Tests**

#### Load Time Testing
```javascript
// tests/e2e/performance.spec.js
test.describe('Performance Testing', () => {
    test('calendar with scenes loads within 2 seconds', async ({ page }) => {
        const startTime = Date.now();
        
        await page.goto('/projects/large-project/calendar');
        
        // Wait for calendar to fully load
        await expect(page.locator('[data-testid="calendar-grid"]')).toBeVisible();
        
        const loadTime = Date.now() - startTime;
        expect(loadTime).toBeLessThan(2000);
    });
    
    test('scene expansion completes within 500ms', async ({ page }) => {
        await page.goto('/projects/test-project/calendar');
        
        const startTime = Date.now();
        await page.click('[data-testid="expand-day-2024-03-15"]');
        await expect(page.locator('.scene-list')).toBeVisible();
        
        const expansionTime = Date.now() - startTime;
        expect(expansionTime).toBeLessThan(500);
    });
});
```

### **Cross-Device E2E Tests**

#### Mobile-Specific Workflows
```javascript
// tests/e2e/mobile.spec.js
test.describe('Mobile Scene Management', () => {
    test.use({ 
        viewport: { width: 375, height: 667 },  // iPhone SE
        isMobile: true,
        hasTouch: true
    });
    
    test('should handle touch-based scene reordering', async ({ page }) => {
        await page.goto('/projects/test-project/calendar');
        await page.tap('[data-testid="expand-day-2024-03-15"]');
        
        // Test touch drag
        const sceneElement = page.locator('[data-testid="scene-1A"]');
        const boundingBox = await sceneElement.boundingBox();
        
        await page.touchscreen.tap(boundingBox.x + 10, boundingBox.y + 10);
        await page.waitForTimeout(500);  // Long press
        
        // Drag to new position
        await page.touchscreen.drag(
            boundingBox.x + 10, 
            boundingBox.y + 10,
            boundingBox.x + 10,
            boundingBox.y + 100
        );
        
        // Verify reorder occurred
        const newOrder = await page.locator('.scene-item').allTextContents();
        expect(newOrder[1]).toContain('1A');
    });
});
```

---

## 📊 Performance Testing

### **Load Testing Strategy**

#### Database Performance Tests
```python
# tests/performance/test_database_performance.py
import time
from django.test import TestCase
from django.test.utils import override_settings

class DatabasePerformanceTest(TestCase):
    def test_large_project_query_performance(self):
        """Test query performance with large dataset"""
        # Create large test dataset
        project = self.create_test_project()
        calendar_days = [
            self.create_calendar_day(project=project, date=f"2024-03-{i:02d}")
            for i in range(1, 32)  # Full month
        ]
        
        # Create 10 scenes per day (300 total)
        scenes = []
        for day in calendar_days:
            for i in range(1, 11):
                scenes.append(self.create_test_scene(
                    calendar_day=day,
                    scene_number=f"{day.date.day}.{i}"
                ))
        
        # Test query performance
        start_time = time.time()
        
        # This is the actual query used by the calendar view
        calendar_data = CalendarDay.objects.filter(
            project=project
        ).prefetch_related(
            'scenes__cast_members',
            'scenes__equipment_requirements'
        ).order_by('date')
        
        # Force evaluation
        list(calendar_data)
        
        query_time = time.time() - start_time
        
        # Should complete within 1 second even with 300 scenes
        self.assertLess(query_time, 1.0)
```

#### Frontend Performance Tests
```javascript
// tests/performance/frontend-performance.test.js
describe('Frontend Performance', () => {
    it('should render large scene lists efficiently', async () => {
        // Create large dataset
        const scenes = Array.from({ length: 200 }, (_, i) => ({
            id: i + 1,
            scene_number: `${i + 1}`,
            description: `Scene ${i + 1} description`,
            estimated_duration: 60
        }));
        
        const startTime = performance.now();
        
        // Render component with large dataset
        render(<SceneList scenes={scenes} />);
        
        const renderTime = performance.now() - startTime;
        
        // Should render within 100ms
        expect(renderTime).toBeLessThan(100);
    });
});
```

---

## 👥 User Acceptance Testing

### **Professional User Testing Protocol**

#### Industry Professional Test Plan
```markdown
# Professional User Testing Session

## Participants
- 1st Assistant Directors (3 participants)
- Producers (2 participants)  
- Production Coordinators (2 participants)

## Test Scenarios

### Scenario 1: Project Setup
1. Create new project
2. Import existing schedule data
3. Set up cast and crew
4. Establish shooting locations

### Scenario 2: Daily Schedule Management
1. Plan shooting day with 8 scenes
2. Assign cast to scenes
3. Identify equipment requirements
4. Resolve scheduling conflicts

### Scenario 3: Schedule Changes
1. Move scenes between days
2. Handle cast availability changes
3. Update equipment requirements
4. Generate updated call sheets

## Success Criteria
- Tasks completed without assistance: >80%
- User satisfaction rating: >4.0/5.0
- Time to complete core tasks: <50% of current workflow
- Zero data loss incidents
```

### **Usability Testing Metrics**

#### Key Performance Indicators
```python
# Track user interaction metrics
class UsabilityMetrics:
    def track_scene_creation_time(self, user_id, start_time, end_time):
        """Track how long it takes users to create scenes"""
        duration = end_time - start_time
        self.log_metric('scene_creation_duration', duration, user_id)
    
    def track_error_rate(self, user_id, action, success):
        """Track user error rates for key actions"""
        self.log_metric('user_error_rate', {
            'action': action,
            'success': success,
            'user_id': user_id
        })
    
    def track_feature_adoption(self, user_id, feature_name):
        """Track which features users actually use"""
        self.log_metric('feature_adoption', {
            'feature': feature_name,
            'user_id': user_id,
            'timestamp': time.time()
        })
```

---

## 🔒 Security Testing

### **Data Security Tests**

#### Permission Enforcement Tests
```python
# tests/security/test_scene_permissions.py
class SceneSecurityTest(TestCase):
    def test_unauthorized_scene_access(self):
        """Test that users cannot access scenes from other projects"""
        user1 = self.create_test_user('user1')
        user2 = self.create_test_user('user2')
        
        project1 = self.create_test_project(owner=user1)
        scene1 = self.create_test_scene(project=project1)
        
        # User2 tries to access User1's scene
        self.client.force_authenticate(user=user2)
        response = self.client.get(f'/api/scenes/{scene1.id}/')
        
        self.assertEqual(response.status_code, 403)
    
    def test_scene_modification_permissions(self):
        """Test scene modification permissions"""
        readonly_user = self.create_test_user('readonly')
        editor_user = self.create_test_user('editor')
        
        project = self.create_test_project()
        scene = self.create_test_scene(project=project)
        
        # Grant different permission levels
        project.add_member(readonly_user, role='viewer')
        project.add_member(editor_user, role='editor')
        
        # Test readonly user cannot modify
        self.client.force_authenticate(user=readonly_user)
        response = self.client.patch(f'/api/scenes/{scene.id}/', {
            'description': 'Modified description'
        })
        self.assertEqual(response.status_code, 403)
        
        # Test editor can modify
        self.client.force_authenticate(user=editor_user)
        response = self.client.patch(f'/api/scenes/{scene.id}/', {
            'description': 'Modified description'
        })
        self.assertEqual(response.status_code, 200)
```

---

## 📈 Continuous Testing Strategy

### **Automated Testing Pipeline**

#### CI/CD Integration
```yaml
# .github/workflows/scene-management-tests.yml
name: Scene Management Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run unit tests
        run: python manage.py test tests.unit --verbosity=2
  
  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v3
      - name: Setup test database
        run: python manage.py migrate --settings=config.test_settings
      - name: Run integration tests
        run: python manage.py test tests.integration --verbosity=2
  
  e2e-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install Playwright
        run: npx playwright install
      - name: Run E2E tests
        run: npx playwright test
  
  performance-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    steps:
      - uses: actions/checkout@v3
      - name: Run performance tests
        run: python manage.py test tests.performance --verbosity=2
```

### **Quality Gates**

#### Automated Quality Checks
```python
# Quality gate enforcement
class QualityGate:
    def __init__(self):
        self.requirements = {
            'test_coverage': 95,
            'performance_threshold': 2.0,  # seconds
            'error_rate_threshold': 0.01,  # 1%
            'user_satisfaction': 4.0       # out of 5
        }
    
    def check_quality_gates(self, test_results):
        gates_passed = []
        
        # Check test coverage
        if test_results['coverage'] >= self.requirements['test_coverage']:
            gates_passed.append('coverage')
        
        # Check performance
        if test_results['avg_response_time'] <= self.requirements['performance_threshold']:
            gates_passed.append('performance')
        
        # Check error rate
        if test_results['error_rate'] <= self.requirements['error_rate_threshold']:
            gates_passed.append('error_rate')
        
        return len(gates_passed) == len(self.requirements)
```

---

## 🎯 Success Criteria

### **Testing Success Metrics**

#### Quantitative Metrics
- **Test Coverage**: >95% code coverage
- **Performance**: All operations <2 seconds
- **Error Rate**: <1% user-facing errors
- **Cross-Browser**: 100% compatibility Chrome, Firefox, Safari
- **Mobile**: 100% feature parity on mobile devices

#### Qualitative Metrics
- **User Satisfaction**: >4.0/5.0 rating from professional users
- **Feature Adoption**: >50% of users using scene features within 30 days
- **Support Tickets**: No increase in support volume
- **Industry Validation**: Positive feedback from film industry professionals

The comprehensive testing strategy ensures that the Movie Magic Stripboard integration meets professional standards while maintaining the reliability and performance users expect from STRIPS.