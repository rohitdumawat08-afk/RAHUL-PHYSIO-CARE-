import unittest
import json
import sys
from app import app
from database import get_db_connection, init_db

class RahulPhysioTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        init_db()

    def test_01_public_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Rahul Physio', response.data)
        self.assertIn(b'7023029646', response.data)
        print("[OK] Public Homepage loads with status 200")

    def test_02_get_public_therapies(self):
        response = self.client.get('/api/therapies')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('therapies', data)
        self.assertGreater(len(data['therapies']), 40)
        print(f"[OK] Public Therapies API returns {len(data['therapies'])} active therapies")

    def test_03_category_filter(self):
        response = self.client.get('/api/therapies?category=Sports%20Injuries')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        for t in data['therapies']:
            self.assertEqual(t['category'], 'Sports Injuries')
        print(f"[OK] Category filter for 'Sports Injuries' returns {len(data['therapies'])} items")

    def test_04_check_service_area(self):
        response = self.client.post('/api/check-area',
            data=json.dumps({'area': 'Pratap Nagar'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['available'])
        self.assertIn('Pratap Nagar', data['area'])
        print("[OK] Locality availability checker returns active coverage")

    def test_05_create_booking(self):
        payload = {
            'patient_name': 'Aarav Sharma',
            'phone': '7023029646',
            'area': 'Sitapura, Jaipur',
            'preferred_date': '2026-09-01',
            'preferred_time': 'Morning: 6:00 AM – 8:00 AM',
            'service_name': 'Low Back Pain Rehabilitation',
            'message': 'Acute lower lumbar spasm since 2 days.'
        }
        response = self.client.post('/api/bookings',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('booking_id', data)
        print(f"[OK] Booking created successfully with ID #{data['booking_id']}")

    def test_06_admin_auth_and_crud(self):
        # 1. Invalid login
        bad_res = self.client.post('/api/admin/login',
            data=json.dumps({'username': 'admin', 'password': 'wrongpassword'}),
            content_type='application/json'
        )
        self.assertEqual(bad_res.status_code, 401)
        print("[OK] Invalid admin credentials correctly rejected (401)")

        # 2. Valid login
        good_res = self.client.post('/api/admin/login',
            data=json.dumps({'username': 'admin', 'password': 'rahul1234'}),
            content_type='application/json'
        )
        self.assertEqual(good_res.status_code, 200)
        print("[OK] Admin login successful with valid credentials")

        # 3. Get admin stats
        stats_res = self.client.get('/api/admin/stats')
        self.assertEqual(stats_res.status_code, 200)
        stats = json.loads(stats_res.data)
        self.assertGreater(stats['total_therapies'], 0)
        print(f"[OK] Admin stats retrieved: {stats}")

        # 4. Add new custom therapy
        new_therapy_data = {
            'name': 'Dry Needling & Myofascial Trigger Therapy',
            'category': 'Physiotherapy Services',
            'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80',
            'short_desc': 'Targeted trigger point deactivation for persistent muscular knots.',
            'full_desc': 'Clinical dry needling combined with soft tissue mobilization to release tight myofascial bands.',
            'price': '850',
            'duration': '45 Mins',
            'status': 'active',
            'indications': 'Chronic myofascial pain, Deep trigger points'
        }
        create_res = self.client.post('/api/admin/therapies',
            data=json.dumps(new_therapy_data),
            content_type='application/json'
        )
        self.assertEqual(create_res.status_code, 201)
        created_data = json.loads(create_res.data)
        therapy_id = created_data['id']
        print(f"[OK] Added new therapy via Admin API with ID #{therapy_id}")

        # 5. Verify it appears on public therapies API
        pub_res = self.client.get('/api/therapies')
        pub_data = json.loads(pub_res.data)
        found = any(t['id'] == therapy_id for t in pub_data['therapies'])
        self.assertTrue(found)
        print("[OK] Newly created therapy automatically appears on the public website!")

        # 6. Update therapy
        new_therapy_data['price'] = '900'
        update_res = self.client.put(f'/api/admin/therapies/{therapy_id}',
            data=json.dumps(new_therapy_data),
            content_type='application/json'
        )
        self.assertEqual(update_res.status_code, 200)
        print("[OK] Therapy updated successfully")

        # 7. Toggle status to inactive
        toggle_res = self.client.post(f'/api/admin/therapies/{therapy_id}/toggle-status')
        self.assertEqual(toggle_res.status_code, 200)
        
        # Verify it's no longer on public list
        pub_res2 = self.client.get('/api/therapies')
        pub_data2 = json.loads(pub_res2.data)
        found_after_inactive = any(t['id'] == therapy_id for t in pub_data2['therapies'])
        self.assertFalse(found_after_inactive)
        print("[OK] Inactive therapy correctly hidden from public visitors")

        # 8. Delete therapy
        del_res = self.client.delete(f'/api/admin/therapies/{therapy_id}')
        self.assertEqual(del_res.status_code, 200)
        print("[OK] Therapy deleted cleanly from database")

        # 9. Check Bookings management
        bookings_res = self.client.get('/api/admin/bookings')
        self.assertEqual(bookings_res.status_code, 200)
        bookings_data = json.loads(bookings_res.data)
        self.assertGreater(len(bookings_data['bookings']), 0)
        booking_id = bookings_data['bookings'][0]['id']

        # Update booking status to confirmed
        status_res = self.client.post(f'/api/admin/bookings/{booking_id}/status',
            data=json.dumps({'status': 'confirmed'}),
            content_type='application/json'
        )
        self.assertEqual(status_res.status_code, 200)
        print(f"[OK] Booking #{booking_id} status updated to 'confirmed'")

if __name__ == '__main__':
    unittest.main()
