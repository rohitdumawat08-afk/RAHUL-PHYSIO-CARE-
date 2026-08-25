# seed_data.py
import sqlite3
import os
from database import get_db_connection, init_db

THERAPIES_DATA = [
    # 1. Orthopedic / Musculoskeletal
    {
        "name": "Low Back Pain Rehabilitation",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Targeted home-based physical therapy for acute and chronic lumbar spine discomfort and disc issues.",
        "full_desc": "Comprehensive home physical therapy focused on lumbar spine decompression, core muscle stabilization, pelvic alignment, and gentle mobility drills. Tailored to alleviate stiffness and restore pain-free movement in everyday activities.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Lumbar strain, Disc bulge, Sciatica, Chronic back stiffness, Postural fatigue"
    },
    {
        "name": "Neck Pain / Cervical Pain Therapy",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Relief and postural correction for cervical spine strain, upper back stiffness, and tech neck.",
        "full_desc": "Personalized cervical spine mobilization, gentle trapezius stretching, scapular stabilization, and ergonomic posture retraining delivered right in the comfort of your home.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Cervical spondylosis, Text neck syndrome, Muscle spasm, Radiating arm discomfort, Neck stiffness"
    },
    {
        "name": "Shoulder Pain Rehabilitation",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Therapeutic care for impingement, glenohumeral joint stiffness, and overhead movement discomfort.",
        "full_desc": "Gentle range of motion exercises, scapular rhythm restoration, and progressive strengthening of rotator cuff and deltoid muscles to enhance shoulder function.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Shoulder impingement, Bursitis, Tendonitis, Muscle weakness, Overhead reaching restriction"
    },
    {
        "name": "Frozen Shoulder (Adhesive Capsulitis)",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Stage-specific mobility restoration and capsular stretching for painful and restricted shoulders.",
        "full_desc": "Carefully structured gentle passive mobilization, active-assisted wand drills, pendulum exercises, and thermal therapy techniques to progressively unlock frozen shoulder stages without aggressive pain flare-ups.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Adhesive capsulitis, Severe movement restriction, Sleep-disturbing shoulder ache"
    },
    {
        "name": "Rotator Cuff Problems Care",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1598256989800-fe5f95da9787?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Non-surgical rehab and strengthening for supraspinatus, infraspinatus, and subscapularis tears or strains.",
        "full_desc": "Progressive resistance training using therapeutic bands, eccentric conditioning, and scapular stabilization to rebuild shoulder stability and functional reach.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Partial rotator cuff tear, Tendinopathy, Overhead lifting difficulty, Weakness"
    },
    {
        "name": "Tennis Elbow Rehabilitation",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Targeted therapy for lateral epicondylitis and forearm extensor tendon overload.",
        "full_desc": "Soft tissue techniques, eccentric forearm extensor loading, forearm wrist flexor/extensor balancing, and grip strength optimization for computer users and racket athletes.",
        "price": "",
        "duration": "40-50 Mins",
        "status": "active",
        "indications": "Lateral epicondyle tenderness, Gripping pain, Forearm muscle fatigue"
    },
    {
        "name": "Golfer’s Elbow Care",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Rehabilitation for medial epicondylitis and repetitive forearm flexor strain.",
        "full_desc": "Progressive wrist flexor eccentric exercises, manual soft tissue mobilization, pronator teres stretching, and functional movement re-education.",
        "price": "",
        "duration": "40-50 Mins",
        "status": "active",
        "indications": "Medial elbow ache, Weak wrist flexion, Repetitive strain discomfort"
    },
    {
        "name": "Wrist & Hand Pain Therapy",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Therapy for carpal tunnel symptoms, De Quervain's tenosynovitis, and wrist joint stiffness.",
        "full_desc": "Median nerve gliding drills, wrist joint mobilization, intrinsic hand muscle strengthening, and ergonomic posture consultation for daily desktop and domestic tasks.",
        "price": "",
        "duration": "40-50 Mins",
        "status": "active",
        "indications": "Carpal tunnel syndrome, De Quervain tenosynovitis, Wrist strain, Post-cast stiffness"
    },
    {
        "name": "Hip Pain Rehabilitation",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Focused exercises for hip bursitis, labral irritation, gluteal tendinopathy, and stiffness.",
        "full_desc": "Gluteus medius/maximus activation, hip joint capsule mobility, pelvic stability training, and functional gait improvement to reduce hip joint stress.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Trochanteric bursitis, Gluteal tendinopathy, Hip joint impingement, Piriformis syndrome"
    },
    {
        "name": "Knee Pain Therapy",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1576091160291-209867018318?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Comprehensive home physical therapy for patellofemoral pain, tendonitis, and joint discomfort.",
        "full_desc": "Quadriceps and VMO strengthening, hamstring flexibility, patellar mobilization, and biomechanical alignment correction to relieve knee strain during walking and stair climbing.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Patellofemoral pain syndrome, Patellar tendonitis, Runner's knee, Knee stiffness"
    },
    {
        "name": "Osteoarthritis (OA) Management",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Low-impact strengthening, joint mobility, and functional preservation for knee and hip arthritis.",
        "full_desc": "Evidence-guided non-impact exercise programs, joint unloading techniques, quadriceps/hamstring strengthening, and gait assist guidance to improve daily comfort and delay surgical intervention.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Knee OA (Grade 1-3), Hip OA, Age-related degenerative joint stiffness"
    },
    {
        "name": "Ankle & Foot Pain Rehabilitation",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Targeted care for Achilles tendinopathy, flat feet discomfort, and chronic ankle stiffness.",
        "full_desc": "Achilles tendon eccentric loading, talocrural joint mobilization, intrinsic foot muscle exercises, and calf complex stretching designed for stable, pain-free walking.",
        "price": "",
        "duration": "40-50 Mins",
        "status": "active",
        "indications": "Achilles tendinitis, Flat foot strain, Ankle impingement, Metatarsalgia"
    },
    {
        "name": "Plantar Fasciitis Relief & Rehab",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Structured morning heel pain management, fascia release, and arch strengthening.",
        "full_desc": "Plantar fascia specific stretching, calf muscle release, windlass mechanism retraining, foot arch dome exercises, and footwear guidance for first-step heel pain.",
        "price": "",
        "duration": "40-50 Mins",
        "status": "active",
        "indications": "First-step morning heel ache, Plantar fascia tightness, Calcaneal spur discomfort"
    },
    {
        "name": "Muscle Strain Rehabilitation",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Phase-based healing and progressive loading for strained muscles across the body.",
        "full_desc": "Acute pain mitigation, isometric-to-isotonic progression, scar tissue remodeling, and flexibility restoration to regain muscle elasticity and prevent re-injury.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Grade 1-2 muscle strains, Post-exercise muscle tearing, Spasm and tenderness"
    },
    {
        "name": "Joint Stiffness Management",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Restoring natural range of motion after immobilization, injury, or inactivity.",
        "full_desc": "Gentle manual passive and active-assisted range of motion drills, capsule stretching, and rhythmic movement patterns to lubricate joints and reduce morning tightness.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Post-immobilization stiffness, Morning joint resistance, Reduced range of motion"
    },
    {
        "name": "Muscle Tightness Release",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Targeted myofascial release, sustained static stretching, and tension relief.",
        "full_desc": "Manual trigger point therapy, sustained stretching protocols, breathing relaxation coordination, and postural unloading for persistently tight muscle groups.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Trapezius tightness, Hamstring shortening, Piriformis tension, Calf tightness"
    },
    {
        "name": "Postural Problems Correction",
        "category": "Orthopedic / Musculoskeletal",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Ergonomic alignment training for kyphosis, rounded shoulders, and anterior pelvic tilt.",
        "full_desc": "Kinesthetic awareness drills, deep spinal stabilizer activation, chest opening stretches, and customized home workstation posture modifications.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Forward head posture, Kyphotic slouching, Desk worker fatigue, Pelvic tilt"
    },

    # 2. Sports Injuries
    {
        "name": "ACL Injury Rehabilitation",
        "category": "Sports Injuries",
        "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Comprehensive non-surgical or post-operative anterior cruciate ligament recovery program.",
        "full_desc": "Step-by-step kinetic chain strengthening, quadriceps-hamstring co-contraction drills, neuromuscular proprioception training, and progressive knee stability protocols.",
        "price": "",
        "duration": "50-60 Mins",
        "status": "active",
        "indications": "ACL tear rehab, Knee instability, Quadriceps inhibition, Deceleration weakness"
    },
    {
        "name": "PCL Injury Rehabilitation",
        "category": "Sports Injuries",
        "image_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Posterior cruciate ligament conditioning and anterior tibiofemoral stabilization.",
        "full_desc": "Focus on isolated quadriceps strengthening, avoiding posterior tibial sag during recovery, open and closed kinetic chain exercises, and dynamic knee control.",
        "price": "",
        "duration": "50-60 Mins",
        "status": "active",
        "indications": "PCL sprain, Posterior knee laxity, Dashboard impact injury recovery"
    },
    {
        "name": "MCL / LCL Injury Rehabilitation",
        "category": "Sports Injuries",
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Collateral ligament healing, coronal stability, and rotational knee control.",
        "full_desc": "Protected range of motion progression, adductor/abductor muscle balancing, frontal plane stability training, and brace-assisted mobility drills.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Medial collateral ligament sprain, Lateral collateral sprain, Varus/valgus stress recovery"
    },
    {
        "name": "Meniscus Injury Rehabilitation",
        "category": "Sports Injuries",
        "image_url": "https://images.unsplash.com/photo-1576091160291-209867018318?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Conservative and post-meniscectomy knee joint unloading and strengthening.",
        "full_desc": "Joint line symptom alleviation, progressive weight-bearing tolerance, deep squat avoidance during acute phase, and knee shock-absorption muscle conditioning.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Meniscal tear, Knee joint line tenderness, Minor knee locking or catching"
    },
    {
        "name": "Ankle Sprain Rehabilitation",
        "category": "Sports Injuries",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Lateral ligament recovery, swelling reduction, and balance/proprioception retraining.",
        "full_desc": "Peroneal muscle strengthening, single-leg balance board drills, dynamic agility transitions, and ankle joint mobilization to prevent chronic instability.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Inversion ankle sprain, ATF ligament strain, Recurrent ankle roll, Swelling"
    },
    {
        "name": "Hamstring Injury Rehabilitation",
        "category": "Sports Injuries",
        "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Eccentric lengthening protocols, sprinting deceleration retraining, and scar remodeling.",
        "full_desc": "Nordic hamstring progressions, lengthening under load, pelvic tilt control, and hip extensor synergy training to safeguard against recurring hamstring pulls.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Biceps femoris strain, Semitendinosus pull, High-speed running injury"
    },
    {
        "name": "Calf Strain Rehabilitation",
        "category": "Sports Injuries",
        "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Gastrocnemius and soleus muscle recovery, plantarflexor loading, and push-off power restoration.",
        "full_desc": "Gentle cross-friction soft tissue work, progressive double to single leg heel raises, soleus bent-knee loading, and explosive push-off reconditioning.",
        "price": "",
        "duration": "45-55 Mins",
        "status": "active",
        "indications": "Tennis leg, Gastrocnemius medial head strain, Sudden acceleration calf pain"
    },
    {
        "name": "Groin Injury Rehabilitation",
        "category": "Sports Injuries",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Adductor longus strengthening, pelvic stability, and cutting/changing direction drills.",
        "full_desc": "Copenhagen adductor exercise protocols, abdominal-pelvic core stabilization, hip internal/external rotation balance, and gradual change-of-direction training.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Adductor strain, Athletic pubalgia discomfort, Kicking sport groin ache"
    },
    {
        "name": "Sports-Related Muscle Injuries",
        "category": "Sports Injuries",
        "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Systematic care for sports impact contusions, muscle fiber tears, and overtraining fatigue.",
        "full_desc": "Comprehensive functional movement screening, targeted active rehabilitation, sports-specific kinetic chain loading, and tissue conditioning.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Direct contact muscle contusion, Overuse strain, Explosive athletic fatigue"
    },
    {
        "name": "Return-to-Sport Rehabilitation",
        "category": "Sports Injuries",
        "image_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Objective criterion-based testing, plyometrics, and sport-specific agility drills.",
        "full_desc": "Limb symmetry testing, multi-planar agility drills, plyometric jump-landing mechanics, cardiovascular conditioning, and psychological readiness assessment for safe sport return.",
        "price": "",
        "duration": "50-60 Mins",
        "status": "active",
        "indications": "Final stage athletic clearance, Agility readiness, Confidence building after injury"
    },

    # 3. Neurological Rehabilitation
    {
        "name": "Stroke Rehabilitation (Home Visit)",
        "category": "Neurological Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Neuroplasticity-driven motor recovery, functional retraining, and tone management at home.",
        "full_desc": "Evidence-based task-oriented training, motor relearning principles, constraint-induced movement strategies, abnormal synergy inhibition, and bed-to-chair transfer practice in the patient's familiar living environment.",
        "price": "",
        "duration": "50-60 Mins",
        "status": "active",
        "indications": "Ischemic/Hemorrhagic stroke recovery, Motor deficit, Functional dependency"
    },
    {
        "name": "Hemiplegia Rehabilitation",
        "category": "Neurological Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Targeted therapy for one-sided weakness, spasticity management, and trunk symmetry.",
        "full_desc": "Bilateral arm training, weight-shifting exercises towards the affected side, tone normalization, scapular protraction facilitation, and stepping coordination.",
        "price": "",
        "duration": "50-60 Mins",
        "status": "active",
        "indications": "Unilateral weakness, Spastic hemiplegic posture, Asymmetric weight bearing"
    },
    {
        "name": "Parkinson’s Disease Rehabilitation",
        "category": "Neurological Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Large-amplitude movement training, freezing alleviation, and postural stability drills.",
        "full_desc": "High-amplitude rhythmic movement exercises, visual/auditory cueing for freezing of gait, axial rotation facilitation, balance perturbations, and fall-risk reduction strategies.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Parkinsonian bradykinesia, Rigidity, Freezing of gait, Postural instability"
    },
    {
        "name": "Balance Problems Therapy",
        "category": "Neurological Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Vestibular and sensory integration drills for unsteadiness and equilibrium issues.",
        "full_desc": "Multi-sensory balance training, narrow base standing, tandem walking, head-eye movement coordination, and perturbed surface balance drills designed for home safety.",
        "price": "",
        "duration": "45-55 Mins",
        "status": "active",
        "indications": "Dysequilibrium, Sensory ataxia, Fear of falling, Unsteady standing"
    },
    {
        "name": "Gait Training & Locomotion",
        "category": "Neurological Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Cadence, step length, and biomechanical correction for impaired walking patterns.",
        "full_desc": "Systematic breakdown of stance and swing phase mechanics, weight transfer drills, assistive device fitting and training (walkers/canes), and indoor obstacle navigation.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Circumductory gait, Scissoring gait, Short step cadence, Trendelenburg lurch"
    },
    {
        "name": "Mobility Training",
        "category": "Neurological Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Bed mobility, sit-to-stand transitions, and safe transfers within the home.",
        "full_desc": "Bridging, rolling, supine-to-sit sequencing, stable chair transfers, toilet transfer assistance techniques, and caregiver ergonomic guidance.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Difficulty rising from bed, Inability to stand unassisted, Wheelchair transitions"
    },
    {
        "name": "Muscle Weakness Rehabilitation",
        "category": "Neurological Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Neuromuscular electrical stimulation guidance and progressive active-assisted muscle activation.",
        "full_desc": "Facilitation of voluntary motor contraction, progressive resistance under neurogenic protocols, fatigue management, and functional limb integration.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Neuropathic weakness, Post-illness motor fatigue, Paretic limb weakness"
    },
    {
        "name": "Coordination Training",
        "category": "Neurological Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Frenkel's exercises and rhythmic stabilization for ataxia and dysmetria.",
        "full_desc": "Repetitive precision target touching, heel-to-shin tracking, rhythmic alternation of limb movements, and fine motor dexterity enhancement drills.",
        "price": "",
        "duration": "40-50 Mins",
        "status": "active",
        "indications": "Cerebellar ataxia, Tremor compensation, Inaccurate limb targeting, Clumsiness"
    },
    {
        "name": "Spinal Cord Injury Rehabilitation",
        "category": "Neurological Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Maximal functional independence, wheelchair skills, and preservation of range of motion.",
        "full_desc": "Tenodesis grip preservation, pressure relief routines, passive range of motion to avoid contractures, trunk balance in sitting, and adapted transfer training.",
        "price": "",
        "duration": "50-60 Mins",
        "status": "active",
        "indications": "Paraplegia/incomplete SCI recovery, Wheelchair propulsion, Contracture prevention"
    },

    # 4. Post-Surgery Rehabilitation
    {
        "name": "Knee Replacement Rehabilitation (TKR)",
        "category": "Post-Surgery Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1576091160291-209867018318?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Post-total knee arthroplasty flexion/extension restoration, swelling management, and walking re-education.",
        "full_desc": "Systematic post-operative protocol: Cryotherapy guidance, gentle knee range of motion (achieving full extension & 90-120° flexion), quadriceps lag correction, straight leg raises, and transition from walker to cane.",
        "price": "",
        "duration": "50-60 Mins",
        "status": "active",
        "indications": "Total Knee Arthroplasty (TKR), Partial Knee Replacement, Post-surgical knee stiffness"
    },
    {
        "name": "Hip Replacement Rehabilitation (THR)",
        "category": "Post-Surgery Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Total hip arthroplasty precaution compliance, abductor strengthening, and limp-free walking.",
        "full_desc": "Adherence to surgical hip precautions, gentle active-assisted hip flexion/abduction, gluteal activation, safe sitting/standing instructions, and independent stair climbing training.",
        "price": "",
        "duration": "50-60 Mins",
        "status": "active",
        "indications": "Total Hip Replacement, Bipolar Hemiarthroplasty, Post-hip surgery mobility deficit"
    },
    {
        "name": "ACL Reconstruction Rehabilitation",
        "category": "Post-Surgery Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Graft protection, full knee extension achievement, and progressive quad re-activation.",
        "full_desc": "Strict milestone-based recovery: Graft healing protection, patellar glide mobilization, terminal knee extension restoration, closed kinetic chain loading, and neuromuscular re-education.",
        "price": "",
        "duration": "50-60 Mins",
        "status": "active",
        "indications": "Post-arthroscopic ACL reconstruction (Hamstring/BTB graft), Meniscus repair"
    },
    {
        "name": "Fracture Rehabilitation & Post-Cast Care",
        "category": "Post-Surgery Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Safely mobilizing joints and regaining strength following orthopedic cast removal or plating/nailing.",
        "full_desc": "Carefully staged post-union physical therapy: Edema reduction, gradual joint mobilization, progressive weight bearing as permitted by surgeon, and atrophy reversal.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Post-Colles fracture, Ankle malleolar fracture, Tibia/Femur plating or nailing"
    },
    {
        "name": "Shoulder Surgery Rehabilitation",
        "category": "Post-Surgery Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Post-arthroscopic rotator cuff repair, subacromial decompression, or Labral repair care.",
        "full_desc": "Sling weaning guidance, passive forward elevation within safe limits, scapular setting, active-assisted range progression, and gradual cuff strengthening without graft compromise.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Post-rotator cuff repair, Bankart repair, Subacromial decompression"
    },
    {
        "name": "Post-Operative Mobility Training",
        "category": "Post-Surgery Rehabilitation",
        "image_url": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Immediate home transition, safe ambulation, deep breathing, and thrombosis prevention.",
        "full_desc": "Chest physical therapy and ankle pumps to prevent post-op complications, confidence-building home ambulation, bathroom accessibility coaching, and safe daily life adaptation.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "General orthopedic/surgical discharge, Initial home ambulation difficulty"
    },

    # 5. Elderly / Home-Based Rehab
    {
        "name": "Elderly Balance Training",
        "category": "Elderly / Home-Based Rehab",
        "image_url": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Gentle, supportive equilibrium exercises tailored to senior citizens in their home.",
        "full_desc": "Static and dynamic balance drills using chair support, weight-shifting exercises, stepping in multiple directions, and ankle-hip balance strategies designed to build steady confidence.",
        "price": "",
        "duration": "45-55 Mins",
        "status": "active",
        "indications": "Age-related balance loss, Postural sway, Fear of losing balance during walking"
    },
    {
        "name": "Senior Fall Prevention Program",
        "category": "Elderly / Home-Based Rehab",
        "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Comprehensive home hazard assessment and physical exercises to prevent dangerous slips and trips.",
        "full_desc": "Assessment of home rug/lighting hazards, lower body reactive stepping drills, dual-task walking training, and floor-to-stand safety strategies for elderly residents.",
        "price": "",
        "duration": "45-55 Mins",
        "status": "active",
        "indications": "History of falls, Uneven gait, Slipping fears, Poor foot clearance"
    },
    {
        "name": "Walking / Gait Training for Seniors",
        "category": "Elderly / Home-Based Rehab",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Restoring steady step symmetry, stride length, and comfortable walking rhythm.",
        "full_desc": "Targeted walking practice across home corridors, posture elevation, foot roll-through mechanics, and ergonomic adjustment of walking canes or frames.",
        "price": "",
        "duration": "40-50 Mins",
        "status": "active",
        "indications": "Shuffling steps, Reduced walking stamina, Stooped walking posture"
    },
    {
        "name": "Senior Strengthening Exercises",
        "category": "Elderly / Home-Based Rehab",
        "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Low-resistance progressive muscle conditioning for quadriceps, glutes, and upper body.",
        "full_desc": "Light resistance band exercises, seated leg extensions, wall push-ups, and calf raises designed to counteract sarcopenia and preserve independent vitality.",
        "price": "",
        "duration": "45-50 Mins",
        "status": "active",
        "indications": "Sarcopenia, Muscle wasting, Difficulty carrying light items or climbing stairs"
    },
    {
        "name": "Elderly Mobility Training",
        "category": "Elderly / Home-Based Rehab",
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Preserving joint flexibility, spinal rotation, and fluid limb movement.",
        "full_desc": "Gentle full-body range of motion routines, seated spinal twists, ankle circles, and shoulder rolls to combat morning stiffness and sedentary limitations.",
        "price": "",
        "duration": "40-50 Mins",
        "status": "active",
        "indications": "General joint stiffness, Prolonged sitting stiffness, Reduced flexibility"
    },
    {
        "name": "Functional Independence Training",
        "category": "Elderly / Home-Based Rehab",
        "image_url": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Empowering seniors to perform daily activities, transfers, and self-care with confidence.",
        "full_desc": "Sit-to-stand drills from various chair heights, reaching for household items, safe turning, and adaptive strategies to minimize reliance on family members for basic movements.",
        "price": "",
        "duration": "45-55 Mins",
        "status": "active",
        "indications": "Difficulty standing from low sofa/bed, Dependency on caregiver for movement"
    },
    {
        "name": "General Deconditioning Rehabilitation",
        "category": "Elderly / Home-Based Rehab",
        "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Gradual reconditioning and stamina building following hospital stay or prolonged bed rest.",
        "full_desc": "Low-intensity cardiovascular endurance, gentle isometric exercises, breathing expansion, and gradual progression of out-of-bed activity for revitalized energy.",
        "price": "",
        "duration": "40-50 Mins",
        "status": "active",
        "indications": "Post-illness weakness, Prolonged bed rest deconditioning, Rapid fatigue"
    },

    # 6. Physiotherapy Services
    {
        "name": "Exercise Therapy",
        "category": "Physiotherapy Services",
        "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Prescribed, customized scientific exercise regimens to restore physiological biomechanics.",
        "full_desc": "Evidence-backed movement therapy tailored to individual assessment findings, focusing on targeted muscle activation, kinetic chain re-education, and gradual resistance progression.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Musculoskeletal imbalance, Chronic pain conditions, Functional movement deficits"
    },
    {
        "name": "Therapeutic Exercises",
        "category": "Physiotherapy Services",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Specific corrective drills designed to address pathology, inflammation, and muscle inhibition.",
        "full_desc": "Carefully selected therapeutic exercises targeting specific tissue healing stages, including isometric contractions, active-assisted drills, and closed chain stabilization.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Post-injury recovery, Joint instability, Neuromuscular inhibition"
    },
    {
        "name": "Stretching & Strengthening",
        "category": "Physiotherapy Services",
        "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Harmonizing flexibility and power across opposing muscle groups for injury prevention.",
        "full_desc": "Systematic agonist-antagonist balance protocols combining PNF stretching, static myofascial lengthening, and progressive resistive overload with elastic bands and bodyweight.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Muscle tightness, Postural strain, Weak postural stabilizers"
    },
    {
        "name": "Manual Therapy",
        "category": "Physiotherapy Services",
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Skilled hands-on techniques to modulate pain, release spasm, and restore joint gliding.",
        "full_desc": "Hands-on clinical techniques including passive joint accessory glides, Maitland/Mulligan mobilization principles, and neurodynamic tension release to restore joint mechanics.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Facet joint locking, Capsular restrictions, Somatic joint dysfunction"
    },
    {
        "name": "Joint Mobility Exercises",
        "category": "Physiotherapy Services",
        "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Targeted active and passive mobility drills to enhance synovial lubrication and arc of motion.",
        "full_desc": "Controlled articular rotations, pendulum exercises, physiological range restoration, and continuous gentle movement drills for stiffened joints.",
        "price": "",
        "duration": "40-50 Mins",
        "status": "active",
        "indications": "Joint hypomobility, Morning arthritic stiffness, Post-immobilization tightness"
    },
    {
        "name": "Soft Tissue Techniques",
        "category": "Physiotherapy Services",
        "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Targeted myofascial release, trigger point pressure, and deep tissue soothing techniques.",
        "full_desc": "Application of specialized manual pressure, transverse friction massage, and myofascial decompression to break pain-spasm cycles and improve localized microcirculation.",
        "price": "",
        "duration": "45-55 Mins",
        "status": "active",
        "indications": "Myofascial trigger points, Chronic muscle knots, Hypertonic musculature"
    },
    {
        "name": "Posture Correction Therapy",
        "category": "Physiotherapy Services",
        "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Structural spinal realignment, deep neck flexor training, and ergonomic posture coaching.",
        "full_desc": "Correction of faulty posture habits, strengthening of deep spinal stabilizers (transversus abdominis, multifidus, deep neck flexors), and ergonomic desk workstation assessment.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Upper crossed syndrome, Lower crossed syndrome, Desk worker neck-back pain"
    },
    {
        "name": "Home Exercise Program (HEP) Design",
        "category": "Physiotherapy Services",
        "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Customized, easy-to-follow illustrated self-care routine for continuous home progress.",
        "full_desc": "Personalized step-by-step written and demonstrated home exercise chart tailored to the patient's exact home equipment, empowering long-term self-management and independence.",
        "price": "",
        "duration": "40-50 Mins",
        "status": "active",
        "indications": "Ongoing maintenance, Self-guided recovery, Prevention of recurrence"
    },
    {
        "name": "Functional Rehabilitation",
        "category": "Physiotherapy Services",
        "image_url": "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=800&q=80",
        "short_desc": "Whole-body multi-joint movement training for everyday tasks, work, and sports.",
        "full_desc": "Simulation of daily living and occupational movements, lifting mechanics, multi-directional lunges, overhead reaches, and whole-body stability for seamless return to daily activities.",
        "price": "",
        "duration": "45-60 Mins",
        "status": "active",
        "indications": "Difficulty with lifting, bending, carrying, or stair climbing in daily routine"
    }
]

def seed_database():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if therapies already exist
    cursor.execute('SELECT COUNT(*) as count FROM therapies')
    count = cursor.fetchone()['count']
    
    if count == 0:
        print("Seeding therapies...")
        for item in THERAPIES_DATA:
            cursor.execute("""
                INSERT INTO therapies (name, category, image_url, short_desc, full_desc, price, duration, status, indications)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["name"],
                item["category"],
                item["image_url"],
                item["short_desc"],
                item["full_desc"],
                item["price"],
                item["duration"],
                item["status"],
                item["indications"]
            ))
        conn.commit()
        print(f"Successfully seeded {len(THERAPIES_DATA)} therapies!")
    else:
        print(f"Database already contains {count} therapies. Skipping seed.")
        
    conn.close()

if __name__ == '__main__':
    seed_database()
