// static/js/main.js

let allTherapies = [];
let currentCategory = 'all';
let currentSearch = '';

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    loadTherapies();
    initBookingForms();
    initAreaChecker();
});

// ----------------- NAVIGATION & UI ----------------- //

function initNavigation() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const closeMobileMenu = document.getElementById('closeMobileMenu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.remove('hidden');
        });
    }

    if (closeMobileMenu && mobileMenu) {
        closeMobileMenu.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
        });
    }

    // Close on navigation link click
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if (mobileMenu) mobileMenu.classList.add('hidden');
        });
    });

    // Category filter pills
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active', 'bg-sky-600', 'text-white'));
            e.currentTarget.classList.add('active', 'bg-sky-600', 'text-white');
            currentCategory = e.currentTarget.getAttribute('data-category') || 'all';
            renderTherapies();
        });
    });

    // Search input listener
    const searchInput = document.getElementById('therapySearchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            currentSearch = e.target.value.toLowerCase().trim();
            renderTherapies();
        });
    }
}

// ----------------- THERAPIES LOADER & RENDERER ----------------- //

async function loadTherapies() {
    const container = document.getElementById('therapiesGrid');
    const countBadge = document.getElementById('therapiesCountBadge');
    
    if (container) {
        container.innerHTML = `
            <div class="col-span-full py-16 text-center">
                <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-sky-600 border-t-transparent"></div>
                <p class="mt-4 text-slate-600 font-medium">Loading specialized physiotherapy services...</p>
            </div>
        `;
    }

    try {
        const response = await fetch('/api/therapies');
        const data = await response.json();
        
        if (data.therapies) {
            allTherapies = data.therapies;
            if (countBadge) {
                countBadge.textContent = `${allTherapies.length} Services Available`;
            }
            populateServiceDropdowns();
            renderTherapies();
        }
    } catch (err) {
        console.error('Error loading therapies:', err);
        if (container) {
            container.innerHTML = `
                <div class="col-span-full py-12 text-center text-red-600">
                    <i class="fa-solid fa-triangle-exclamation text-3xl mb-2"></i>
                    <p class="font-medium">Failed to load therapies. Please refresh or call 7023029646.</p>
                </div>
            `;
        }
    }
}

function renderTherapies() {
    const container = document.getElementById('therapiesGrid');
    if (!container) return;

    const filtered = allTherapies.filter(item => {
        const matchesCategory = currentCategory === 'all' || 
            item.category.toLowerCase().trim() === currentCategory.toLowerCase().trim();
        
        const searchLower = currentSearch;
        const matchesSearch = !searchLower || 
            item.name.toLowerCase().includes(searchLower) ||
            item.short_desc.toLowerCase().includes(searchLower) ||
            (item.indications && item.indications.toLowerCase().includes(searchLower)) ||
            item.category.toLowerCase().includes(searchLower);

        return matchesCategory && matchesSearch;
    });

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="col-span-full bg-white rounded-2xl p-12 text-center border border-slate-200 shadow-sm">
                <div class="w-16 h-16 bg-sky-50 text-sky-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i class="fa-solid fa-stethoscope text-2xl"></i>
                </div>
                <h3 class="text-xl font-bold text-slate-800 mb-2">No matching therapies found</h3>
                <p class="text-slate-500 max-w-md mx-auto mb-6">
                    Looking for a specific condition or rehabilitation therapy? We customize home care for various musculoskeletal and neuro conditions.
                </p>
                <button onclick="resetFilters()" class="inline-flex items-center gap-2 px-5 py-2.5 bg-sky-600 text-white rounded-xl font-semibold hover:bg-sky-700 transition">
                    <i class="fa-solid fa-rotate-left"></i> View All Services
                </button>
            </div>
        `;
        return;
    }

    container.innerHTML = filtered.map(t => {
        const priceDisplay = (t.price && t.price.toString().trim() !== '' && t.price.toString().trim() !== '0')
            ? `<span class="text-emerald-700 font-bold bg-emerald-50 px-3 py-1 rounded-full text-sm flex items-center gap-1">
                 <i class="fa-solid fa-indian-rupee-sign text-xs"></i>${t.price}
               </span>`
            : `<span class="text-sky-800 font-medium bg-sky-50 px-3 py-1 rounded-full text-xs flex items-center gap-1">
                 <i class="fa-solid fa-clipboard-check text-xs"></i> Contact for price
               </span>`;

        return `
            <div class="therapy-card bg-white rounded-2xl overflow-hidden border border-slate-200/80 shadow-sm flex flex-col justify-between">
                <div>
                    <div class="relative h-48 w-full overflow-hidden bg-slate-100">
                        <img src="${t.image_url}" alt="${t.name}" 
                             class="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
                             onerror="this.src='https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80'">
                        <div class="absolute top-3 left-3 bg-white/95 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold text-sky-800 shadow-sm border border-sky-100">
                            ${t.category}
                        </div>
                        <div class="absolute bottom-3 right-3 bg-slate-900/80 backdrop-blur-md text-white px-2.5 py-0.5 rounded-lg text-xs font-medium flex items-center gap-1">
                            <i class="fa-regular fa-clock text-[10px]"></i> ${t.duration || '45-60 Mins'}
                        </div>
                    </div>
                    
                    <div class="p-6">
                        <div class="flex items-center justify-between gap-2 mb-2">
                            <span class="text-xs font-semibold uppercase tracking-wider text-teal-600 flex items-center gap-1">
                                <span class="w-1.5 h-1.5 rounded-full bg-teal-500"></span> Home Visit Care
                            </span>
                            ${priceDisplay}
                        </div>
                        
                        <h3 class="text-lg font-bold text-slate-900 mb-2 leading-snug hover:text-sky-600 transition cursor-pointer" onclick="openTherapyModal(${t.id})">
                            ${t.name}
                        </h3>
                        
                        <p class="text-slate-600 text-sm leading-relaxed line-clamp-3 mb-4">
                            ${t.short_desc}
                        </p>

                        ${t.indications ? `
                            <div class="mb-4">
                                <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">Key Focus</span>
                                <div class="flex flex-wrap gap-1">
                                    ${t.indications.split(',').slice(0, 2).map(ind => `
                                        <span class="inline-block bg-slate-100 text-slate-600 text-[11px] px-2 py-0.5 rounded-md font-medium">
                                            ${ind.trim()}
                                        </span>
                                    `).join('')}
                                </div>
                            </div>
                        ` : ''}
                    </div>
                </div>

                <div class="p-6 pt-0 border-t border-slate-100 flex items-center gap-2 mt-auto">
                    <button onclick="openTherapyModal(${t.id})" 
                            class="flex-1 py-2.5 px-3 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-xl transition flex items-center justify-center gap-1.5">
                        <i class="fa-regular fa-eye"></i> Details
                    </button>
                    <button onclick="openBookingModalWithTherapy('${escapeHtml(t.name)}')" 
                            class="flex-1 py-2.5 px-3 bg-sky-600 hover:bg-sky-700 text-white text-xs font-semibold rounded-xl shadow-sm hover:shadow transition flex items-center justify-center gap-1.5">
                        <i class="fa-regular fa-calendar-check"></i> Book Visit
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function resetFilters() {
    currentCategory = 'all';
    currentSearch = '';
    const searchInput = document.getElementById('therapySearchInput');
    if (searchInput) searchInput.value = '';
    
    document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.getAttribute('data-category') === 'all') {
            btn.classList.add('active', 'bg-sky-600', 'text-white');
        } else {
            btn.classList.remove('active', 'bg-sky-600', 'text-white');
        }
    });
    renderTherapies();
}

function filterByCategoryFromCard(categoryName) {
    currentCategory = categoryName;
    document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.getAttribute('data-category') === categoryName) {
            btn.classList.add('active', 'bg-sky-600', 'text-white');
        } else {
            btn.classList.remove('active', 'bg-sky-600', 'text-white');
        }
    });
    
    const servicesSection = document.getElementById('services');
    if (servicesSection) {
        servicesSection.scrollIntoView({ behavior: 'smooth' });
    }
    renderTherapies();
}

// ----------------- THERAPY DETAIL MODAL ----------------- //

function openTherapyModal(therapyId) {
    const therapy = allTherapies.find(t => t.id === therapyId);
    if (!therapy) return;

    const modal = document.getElementById('therapyDetailModal');
    const content = document.getElementById('therapyModalContent');
    if (!modal || !content) return;

    const priceHtml = (therapy.price && therapy.price.toString().trim() !== '' && therapy.price.toString().trim() !== '0')
        ? `<div class="bg-emerald-50 border border-emerald-200 rounded-xl p-3 text-center">
             <span class="text-xs text-emerald-600 font-semibold uppercase block">Service Price</span>
             <span class="text-xl font-bold text-emerald-800">₹${therapy.price}</span>
           </div>`
        : `<div class="bg-sky-50 border border-sky-200 rounded-xl p-3 text-center">
             <span class="text-xs text-sky-600 font-semibold uppercase block">Fee Structure</span>
             <span class="text-base font-bold text-sky-900">Price on consultation</span>
           </div>`;

    content.innerHTML = `
        <div class="relative h-64 md:h-72 w-full overflow-hidden rounded-t-2xl bg-slate-900">
            <img src="${therapy.image_url}" alt="${therapy.name}" class="w-full h-full object-cover opacity-90">
            <button onclick="closeTherapyModal()" class="absolute top-4 right-4 bg-white/90 hover:bg-white text-slate-800 rounded-full w-9 h-9 flex items-center justify-center shadow-lg transition">
                <i class="fa-solid fa-xmark text-lg"></i>
            </button>
            <div class="absolute bottom-4 left-4 right-4 flex flex-wrap items-center justify-between gap-2">
                <span class="bg-white/95 backdrop-blur-md px-3 py-1 rounded-full text-xs font-bold text-sky-800 shadow">
                    ${therapy.category}
                </span>
                <span class="bg-slate-900/80 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold text-white">
                    <i class="fa-regular fa-clock mr-1"></i> ${therapy.duration || '45-60 Mins'} per visit
                </span>
            </div>
        </div>
        
        <div class="p-6 md:p-8 space-y-6">
            <div>
                <h2 class="text-2xl md:text-3xl font-extrabold text-slate-900 mb-2">${therapy.name}</h2>
                <p class="text-slate-600 font-medium leading-relaxed">${therapy.short_desc}</p>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                ${priceHtml}
                <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
                    <span class="text-xs text-slate-500 font-semibold uppercase block">Service Type</span>
                    <span class="text-base font-bold text-slate-800">Home Visit (Doorstep Jaipur)</span>
                </div>
            </div>

            <div>
                <h4 class="text-sm font-bold text-slate-900 uppercase tracking-wider mb-2 flex items-center gap-2">
                    <i class="fa-solid fa-notes-medical text-sky-600"></i> Comprehensive Clinical Overview
                </h4>
                <div class="bg-slate-50 p-4 rounded-xl text-slate-700 text-sm leading-relaxed border border-slate-100">
                    ${therapy.full_desc}
                </div>
            </div>

            ${therapy.indications ? `
                <div>
                    <h4 class="text-sm font-bold text-slate-900 uppercase tracking-wider mb-2 flex items-center gap-2">
                        <i class="fa-solid fa-list-check text-teal-600"></i> Indications & Suitable For
                    </h4>
                    <div class="flex flex-wrap gap-2">
                        ${therapy.indications.split(',').map(item => `
                            <span class="bg-teal-50 text-teal-800 border border-teal-100 px-3 py-1 rounded-lg text-xs font-medium">
                                <i class="fa-solid fa-check text-[10px] mr-1 text-teal-600"></i> ${item.trim()}
                            </span>
                        `).join('')}
                    </div>
                </div>
            ` : ''}

            <div class="bg-sky-50/70 border border-sky-100 rounded-2xl p-4 flex items-start gap-3 text-sm text-sky-900">
                <i class="fa-solid fa-circle-info text-sky-600 mt-0.5 text-base"></i>
                <div>
                    <strong class="font-semibold block">Home Visit Note:</strong>
                    All essential physical therapy assessment tools and therapeutic exercise equipment are brought directly to your home. Prior appointment is recommended.
                </div>
            </div>

            <div class="pt-4 border-t border-slate-200 flex flex-col sm:flex-row gap-3">
                <a href="tel:7023029646" class="flex-1 py-3 px-4 bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold rounded-xl text-center transition flex items-center justify-center gap-2">
                    <i class="fa-solid fa-phone text-sky-600"></i> Call 7023029646
                </a>
                <button onclick="closeTherapyModal(); openBookingModalWithTherapy('${escapeHtml(therapy.name)}')" 
                        class="flex-1 py-3 px-4 bg-sky-600 hover:bg-sky-700 text-white font-bold rounded-xl shadow-md hover:shadow-lg text-center transition flex items-center justify-center gap-2">
                    <i class="fa-regular fa-calendar-check"></i> Book Home Visit
                </button>
            </div>
        </div>
    `;

    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function closeTherapyModal() {
    const modal = document.getElementById('therapyDetailModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// ----------------- BOOKING MODAL & FLOW ----------------- //

function populateServiceDropdowns() {
    const selects = [
        document.getElementById('serviceSelect'),
        document.getElementById('modalServiceSelect')
    ];

    selects.forEach(select => {
        if (!select) return;
        
        // Preserve first placeholder option
        select.innerHTML = '<option value="">-- Select Required Physiotherapy / Therapy --</option>';
        
        const categories = {};
        allTherapies.forEach(t => {
            if (!categories[t.category]) categories[t.category] = [];
            categories[t.category].push(t);
        });

        for (const [catName, therapies] of Object.entries(categories)) {
            const optgroup = document.createElement('optgroup');
            optgroup.label = catName;
            
            therapies.forEach(t => {
                const opt = document.createElement('option');
                opt.value = t.name;
                opt.textContent = t.name;
                optgroup.appendChild(opt);
            });
            select.appendChild(optgroup);
        }
    });
}

function openBookingModalWithTherapy(therapyName) {
    const modal = document.getElementById('bookingModal');
    const select = document.getElementById('modalServiceSelect');
    
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        
        if (select && therapyName) {
            select.value = therapyName;
        }
    }
}

function closeBookingModal() {
    const modal = document.getElementById('bookingModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

function initBookingForms() {
    // 1. Inline Homepage Booking Form
    const inlineForm = document.getElementById('homeBookingForm');
    if (inlineForm) {
        inlineForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await handleBookingSubmission(inlineForm, false);
        });
    }

    // 2. Modal Booking Form
    const modalForm = document.getElementById('modalBookingForm');
    if (modalForm) {
        modalForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await handleBookingSubmission(modalForm, true);
        });
    }

    // 3. Contact Section Form
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await handleContactSubmission(contactForm);
        });
    }
}

async function handleBookingSubmission(formElement, isModal) {
    const submitBtn = formElement.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Submit';

    const formData = {
        patient_name: formElement.querySelector('[name="patient_name"]')?.value || '',
        phone: formElement.querySelector('[name="phone"]')?.value || '',
        area: formElement.querySelector('[name="area"]')?.value || '',
        preferred_date: formElement.querySelector('[name="preferred_date"]')?.value || '',
        preferred_time: formElement.querySelector('[name="preferred_time"]')?.value || '',
        service_name: formElement.querySelector('[name="service_name"]')?.value || '',
        message: formElement.querySelector('[name="message"]')?.value || ''
    };

    // Quick client-side validation
    if (!formData.patient_name || !formData.phone || !formData.area || !formData.preferred_date || !formData.preferred_time || !formData.service_name) {
        Swal.fire({
            icon: 'warning',
            title: 'Incomplete Details',
            text: 'Please fill in all required fields to request your home visit.',
            confirmButtonColor: '#0284c7'
        });
        return;
    }

    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i class="fa-solid fa-spinner animate-spin mr-2"></i> Submitting Request...`;
    }

    try {
        const response = await fetch('/api/bookings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            formElement.reset();
            if (isModal) closeBookingModal();

            const waText = encodeURIComponent(
                `Hello Rahul Physio! I have booked a Home Visit Physiotherapy appointment.\n` +
                `*Patient Name:* ${formData.patient_name}\n` +
                `*Phone:* ${formData.phone}\n` +
                `*Area:* ${formData.area}\n` +
                `*Preferred Date:* ${formData.preferred_date}\n` +
                `*Time Slot:* ${formData.preferred_time}\n` +
                `*Service:* ${formData.service_name}\n` +
                `*Note:* ${formData.message || 'None'}\n` +
                `Please confirm my slot. Thank you!`
            );
            const waUrl = `https://wa.me/917023029646?text=${waText}`;

            Swal.fire({
                icon: 'success',
                title: 'Home Visit Requested!',
                html: `
                    <div class="text-left space-y-3 text-sm text-slate-700">
                        <p class="font-semibold text-emerald-800 bg-emerald-50 p-3 rounded-lg border border-emerald-200">
                            ✓ Your appointment request #RP-${result.booking_id} has been registered!
                        </p>
                        <p>We will contact you shortly to confirm your therapist home-visit slot.</p>
                        <p class="text-xs text-slate-500 font-medium italic">Prior appointment is recommended.</p>
                        <div class="pt-2">
                            <a href="${waUrl}" target="_blank" class="w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl inline-flex items-center justify-center gap-2 shadow transition">
                                <i class="fa-brands fa-whatsapp text-lg"></i> Open WhatsApp Confirmation
                            </a>
                        </div>
                    </div>
                `,
                showCloseButton: true,
                confirmButtonText: 'Done',
                confirmButtonColor: '#0284c7'
            });
        } else {
            throw new Error(result.error || 'Failed to submit appointment request');
        }
    } catch (err) {
        console.error('Booking submission error:', err);
        Swal.fire({
            icon: 'error',
            title: 'Submission Failed',
            text: err.message || 'Unable to submit booking. Please call 7023029646 directly.',
            confirmButtonColor: '#0284c7'
        });
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    }
}

async function handleContactSubmission(formElement) {
    const name = formElement.querySelector('[name="name"]')?.value || '';
    const phone = formElement.querySelector('[name="phone"]')?.value || '';
    const message = formElement.querySelector('[name="message"]')?.value || '';

    if (!name || !phone) {
        Swal.fire({
            icon: 'warning',
            title: 'Missing Info',
            text: 'Please enter your name and phone number.',
            confirmButtonColor: '#0284c7'
        });
        return;
    }

    const waText = encodeURIComponent(
        `Hello Rahul Physio! My name is ${name} (Phone: ${phone}).\nMessage: ${message || 'I have an inquiry regarding home-visit physiotherapy in Jaipur.'}`
    );
    const waUrl = `https://wa.me/917023029646?text=${waText}`;

    Swal.fire({
        icon: 'success',
        title: 'Thank You!',
        html: `
            <p class="text-sm text-slate-600 mb-4">Your message was recorded. You can also connect immediately on WhatsApp or Phone.</p>
            <a href="${waUrl}" target="_blank" class="inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-xl transition shadow">
                <i class="fa-brands fa-whatsapp text-lg"></i> Chat on WhatsApp (7023029646)
            </a>
        `,
        confirmButtonColor: '#0284c7'
    });

    formElement.reset();
}

// ----------------- LOCALITY AVAILABILITY CHECKER ----------------- //

function initAreaChecker() {
    const checkBtn = document.getElementById('checkAreaBtn');
    const areaInput = document.getElementById('areaCheckInput');
    const resultBox = document.getElementById('areaCheckResult');

    if (checkBtn && areaInput && resultBox) {
        checkBtn.addEventListener('click', async () => {
            const query = areaInput.value.trim();
            if (!query) {
                resultBox.innerHTML = `
                    <div class="p-3 bg-amber-50 border border-amber-200 text-amber-800 rounded-xl text-sm font-medium">
                        Please enter your Jaipur area or colony name (e.g. Pratap Nagar, Sitapura, Vaishali Nagar).
                    </div>
                `;
                resultBox.classList.remove('hidden');
                return;
            }

            resultBox.innerHTML = `
                <div class="p-3 bg-sky-50 text-sky-700 rounded-xl text-sm font-medium flex items-center gap-2">
                    <i class="fa-solid fa-spinner animate-spin"></i> Checking doorstep physiotherapy coverage for ${query}...
                </div>
            `;
            resultBox.classList.remove('hidden');

            try {
                const res = await fetch('/api/check-area', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ area: query })
                });
                const data = await res.json();

                resultBox.innerHTML = `
                    <div class="p-4 bg-emerald-50 border border-emerald-200 text-emerald-900 rounded-2xl text-sm shadow-sm space-y-2">
                        <div class="flex items-center gap-2 font-bold text-emerald-800">
                            <i class="fa-solid fa-circle-check text-emerald-600 text-lg"></i>
                            Home Visit Active in ${data.area || query}!
                        </div>
                        <p class="text-xs text-slate-600">${data.message}</p>
                        <div class="pt-2 flex flex-wrap gap-2">
                            <a href="tel:7023029646" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-sky-600 hover:bg-sky-700 text-white rounded-lg font-semibold text-xs transition">
                                <i class="fa-solid fa-phone"></i> Call Now
                            </a>
                            <button onclick="openBookingModalWithTherapy('')" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold text-xs transition">
                                <i class="fa-regular fa-calendar-check"></i> Book Home Visit
                            </button>
                        </div>
                    </div>
                `;
            } catch (err) {
                resultBox.innerHTML = `
                    <div class="p-3 bg-slate-100 text-slate-700 rounded-xl text-sm">
                        Home visits are available across Jaipur. Please call 7023029646 to confirm your slot.
                    </div>
                `;
            }
        });
    }
}

// Utility to escape HTML strings
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
