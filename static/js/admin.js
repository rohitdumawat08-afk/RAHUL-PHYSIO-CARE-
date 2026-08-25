// static/js/admin.js

let adminTherapies = [];
let adminBookings = [];
let currentTab = 'therapies';

document.addEventListener('DOMContentLoaded', () => {
    initAdminTabs();
    loadDashboardStats();
    loadAdminTherapies();
    loadAdminBookings();
    initAdminModals();
    initImageUpload();
});

// ----------------- TABS & STATS ----------------- //

function initAdminTabs() {
    const tabBtns = document.querySelectorAll('.admin-tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const targetTab = e.currentTarget.getAttribute('data-tab');
            switchAdminTab(targetTab);
        });
    });
}

function switchAdminTab(tabName) {
    currentTab = tabName;
    document.querySelectorAll('.admin-tab-btn').forEach(btn => {
        if (btn.getAttribute('data-tab') === tabName) {
            btn.classList.add('bg-sky-600', 'text-white', 'shadow-sm');
            btn.classList.remove('text-slate-600', 'hover:bg-slate-100');
        } else {
            btn.classList.remove('bg-sky-600', 'text-white', 'shadow-sm');
            btn.classList.add('text-slate-600', 'hover:bg-slate-100');
        }
    });

    document.querySelectorAll('.admin-tab-content').forEach(content => {
        if (content.id === `tab-${tabName}`) {
            content.classList.remove('hidden');
        } else {
            content.classList.add('hidden');
        }
    });
}

async function loadDashboardStats() {
    try {
        const res = await fetch('/api/admin/stats');
        if (res.status === 401) {
            window.location.href = '/admin/login';
            return;
        }
        const stats = await res.json();
        
        document.getElementById('statTotalTherapies').textContent = stats.total_therapies || 0;
        document.getElementById('statActiveTherapies').textContent = stats.active_therapies || 0;
        document.getElementById('statInactiveTherapies').textContent = stats.inactive_therapies || 0;
        document.getElementById('statTotalBookings').textContent = stats.total_bookings || 0;
        document.getElementById('statPendingBookings').textContent = stats.pending_bookings || 0;
    } catch (err) {
        console.error('Error fetching admin stats:', err);
    }
}

// ----------------- THERAPIES CRUD ----------------- //

async function loadAdminTherapies() {
    const tableBody = document.getElementById('adminTherapiesTableBody');
    if (!tableBody) return;

    const category = document.getElementById('adminCategoryFilter')?.value || '';
    const status = document.getElementById('adminStatusFilter')?.value || '';
    const search = document.getElementById('adminTherapySearch')?.value || '';

    try {
        const url = new URL('/api/admin/therapies', window.location.origin);
        if (category) url.searchParams.append('category', category);
        if (status) url.searchParams.append('status', status);
        if (search) url.searchParams.append('search', search);

        const res = await fetch(url);
        const data = await res.json();

        if (data.therapies) {
            adminTherapies = data.therapies;
            renderAdminTherapiesTable();
        }
    } catch (err) {
        console.error('Error loading admin therapies:', err);
    }
}

function renderAdminTherapiesTable() {
    const tableBody = document.getElementById('adminTherapiesTableBody');
    if (!tableBody) return;

    if (adminTherapies.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="px-6 py-12 text-center text-slate-500">
                    <i class="fa-solid fa-folder-open text-3xl mb-2 text-slate-400"></i>
                    <p class="font-medium">No therapies found matching the criteria.</p>
                </td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = adminTherapies.map(t => {
        const isActive = t.status === 'active';
        const statusBadge = isActive
            ? `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">
                 <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Active
               </span>`
            : `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-600">
                 <span class="w-1.5 h-1.5 rounded-full bg-slate-400"></span> Inactive
               </span>`;

        const priceText = (t.price && t.price.toString().trim() !== '' && t.price.toString().trim() !== '0')
            ? `₹${t.price}`
            : '<span class="text-xs text-slate-400 italic">Consultation</span>';

        return `
            <tr class="hover:bg-slate-50/80 transition border-b border-slate-100">
                <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                        <img src="${t.image_url}" alt="${t.name}" 
                             class="w-12 h-12 rounded-xl object-cover border border-slate-200 shadow-sm"
                             onerror="this.src='https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80'">
                        <div>
                            <span class="font-bold text-slate-900 block text-sm">${t.name}</span>
                            <span class="text-xs text-slate-500">${t.duration || '45-60 Mins'}</span>
                        </div>
                    </div>
                </td>
                <td class="px-6 py-4 text-xs font-medium text-slate-700">
                    <span class="bg-sky-50 text-sky-700 px-2.5 py-1 rounded-lg border border-sky-100 font-semibold">
                        ${t.category}
                    </span>
                </td>
                <td class="px-6 py-4 text-xs font-bold text-slate-800">
                    ${priceText}
                </td>
                <td class="px-6 py-4">
                    ${statusBadge}
                </td>
                <td class="px-6 py-4 text-xs text-slate-500 max-w-xs truncate" title="${escapeHtml(t.short_desc)}">
                    ${escapeHtml(t.short_desc)}
                </td>
                <td class="px-6 py-4 text-right whitespace-nowrap">
                    <div class="inline-flex items-center gap-2">
                        <button onclick="toggleTherapyStatus(${t.id})" 
                                class="p-2 rounded-lg text-xs font-semibold ${isActive ? 'text-amber-700 hover:bg-amber-50' : 'text-emerald-700 hover:bg-emerald-50'} transition"
                                title="${isActive ? 'Deactivate' : 'Activate'}">
                            <i class="fa-solid ${isActive ? 'fa-eye-slash' : 'fa-eye'}"></i>
                        </button>
                        <button onclick="openEditTherapyModal(${t.id})" 
                                class="p-2 rounded-lg text-xs font-semibold text-sky-700 hover:bg-sky-50 transition"
                                title="Edit Therapy">
                            <i class="fa-solid fa-pen-to-square"></i>
                        </button>
                        <button onclick="confirmDeleteTherapy(${t.id}, '${escapeHtml(t.name)}')" 
                                class="p-2 rounded-lg text-xs font-semibold text-rose-600 hover:bg-rose-50 transition"
                                title="Delete Therapy">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// ----------------- ADD & EDIT THERAPY MODALS ----------------- //

function openAddTherapyModal() {
    const modal = document.getElementById('therapyFormModal');
    const form = document.getElementById('therapyForm');
    const title = document.getElementById('therapyModalTitle');
    
    if (!modal || !form) return;
    
    form.reset();
    document.getElementById('therapyIdInput').value = '';
    document.getElementById('imagePreview').src = 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80';
    document.getElementById('imagePreviewContainer').classList.remove('hidden');
    document.getElementById('therapyStatusInput').value = 'active';
    
    title.textContent = 'Add New Specialized Therapy';
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function openEditTherapyModal(therapyId) {
    const therapy = adminTherapies.find(t => t.id === therapyId);
    if (!therapy) return;

    const modal = document.getElementById('therapyFormModal');
    const form = document.getElementById('therapyForm');
    const title = document.getElementById('therapyModalTitle');
    
    if (!modal || !form) return;

    document.getElementById('therapyIdInput').value = therapy.id;
    document.getElementById('therapyNameInput').value = therapy.name;
    document.getElementById('therapyCategoryInput').value = therapy.category;
    document.getElementById('therapyImageUrlInput').value = therapy.image_url;
    document.getElementById('therapyDurationInput').value = therapy.duration || '45-60 Mins';
    document.getElementById('therapyPriceInput').value = therapy.price || '';
    document.getElementById('therapyStatusInput').value = therapy.status || 'active';
    document.getElementById('therapyShortDescInput').value = therapy.short_desc;
    document.getElementById('therapyFullDescInput').value = therapy.full_desc;
    document.getElementById('therapyIndicationsInput').value = therapy.indications || '';
    
    document.getElementById('imagePreview').src = therapy.image_url || 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80';
    document.getElementById('imagePreviewContainer').classList.remove('hidden');

    title.textContent = `Edit Therapy: ${therapy.name}`;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

function closeTherapyFormModal() {
    const modal = document.getElementById('therapyFormModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

async function handleTherapyFormSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;

    const id = document.getElementById('therapyIdInput').value;
    const data = {
        name: document.getElementById('therapyNameInput').value.trim(),
        category: document.getElementById('therapyCategoryInput').value.trim(),
        image_url: document.getElementById('therapyImageUrlInput').value.trim(),
        duration: document.getElementById('therapyDurationInput').value.trim() || '45-60 Mins',
        price: document.getElementById('therapyPriceInput').value.trim(),
        status: document.getElementById('therapyStatusInput').value,
        short_desc: document.getElementById('therapyShortDescInput').value.trim(),
        full_desc: document.getElementById('therapyFullDescInput').value.trim(),
        indications: document.getElementById('therapyIndicationsInput').value.trim()
    };

    if (!data.name || !data.category || !data.short_desc || !data.full_desc) {
        Swal.fire({
            icon: 'warning',
            title: 'Missing Required Fields',
            text: 'Please fill in Therapy Name, Category, Short Description, and Full Description.',
            confirmButtonColor: '#0284c7'
        });
        return;
    }

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner animate-spin mr-2"></i> Saving...';

    try {
        const url = id ? `/api/admin/therapies/${id}` : '/api/admin/therapies';
        const method = id ? 'PUT' : 'POST';

        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (res.ok && result.success) {
            closeTherapyFormModal();
            Swal.fire({
                icon: 'success',
                title: id ? 'Therapy Updated!' : 'Therapy Added!',
                text: id ? 'Changes saved to database and live website.' : 'New therapy is now live on the public website.',
                timer: 1800,
                showConfirmButton: false
            });
            loadAdminTherapies();
            loadDashboardStats();
        } else {
            throw new Error(result.error || 'Failed to save therapy');
        }
    } catch (err) {
        Swal.fire({
            icon: 'error',
            title: 'Save Failed',
            text: err.message,
            confirmButtonColor: '#0284c7'
        });
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
}

async function toggleTherapyStatus(therapyId) {
    try {
        const res = await fetch(`/api/admin/therapies/${therapyId}/toggle-status`, { method: 'POST' });
        const data = await res.json();
        if (res.ok && data.success) {
            loadAdminTherapies();
            loadDashboardStats();
        } else {
            Swal.fire('Error', data.error || 'Could not toggle status', 'error');
        }
    } catch (err) {
        console.error(err);
    }
}

function confirmDeleteTherapy(therapyId, therapyName) {
    Swal.fire({
        title: 'Delete Therapy?',
        html: `Are you sure you want to permanently delete <strong>"${therapyName}"</strong>?<br><span class="text-xs text-rose-600">It will be immediately removed from the public website.</span>`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#e11d48',
        cancelButtonColor: '#64748b',
        confirmButtonText: 'Yes, Delete Therapy',
        cancelButtonText: 'Cancel'
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                const res = await fetch(`/api/admin/therapies/${therapyId}`, { method: 'DELETE' });
                const data = await res.json();
                if (res.ok && data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Deleted!',
                        text: 'Therapy has been deleted.',
                        timer: 1500,
                        showConfirmButton: false
                    });
                    loadAdminTherapies();
                    loadDashboardStats();
                } else {
                    Swal.fire('Error', data.error || 'Failed to delete therapy', 'error');
                }
            } catch (err) {
                Swal.fire('Error', 'Server communication failure', 'error');
            }
        }
    });
}

// ----------------- IMAGE UPLOAD ----------------- //

function initImageUpload() {
    const fileInput = document.getElementById('therapyImageFileInput');
    const urlInput = document.getElementById('therapyImageUrlInput');
    const preview = document.getElementById('imagePreview');
    const previewContainer = document.getElementById('imagePreviewContainer');
    const uploadBtn = document.getElementById('uploadImageBtn');

    if (fileInput && uploadBtn) {
        fileInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('image', file);

            uploadBtn.innerHTML = '<i class="fa-solid fa-spinner animate-spin"></i> Uploading...';
            uploadBtn.disabled = true;

            try {
                const res = await fetch('/api/admin/upload-image', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();

                if (res.ok && data.success) {
                    urlInput.value = data.url;
                    preview.src = data.url;
                    previewContainer.classList.remove('hidden');
                    Swal.fire({
                        icon: 'success',
                        title: 'Image Uploaded!',
                        timer: 1400,
                        showConfirmButton: false
                    });
                } else {
                    Swal.fire('Upload Failed', data.error || 'Invalid file format', 'error');
                }
            } catch (err) {
                Swal.fire('Upload Failed', 'Server error uploading image', 'error');
            } finally {
                uploadBtn.innerHTML = '<i class="fa-solid fa-upload mr-1"></i> Upload File';
                uploadBtn.disabled = false;
            }
        });
    }

    if (urlInput && preview) {
        urlInput.addEventListener('input', (e) => {
            const val = e.target.value.trim();
            if (val) {
                preview.src = val;
                previewContainer.classList.remove('hidden');
            }
        });
    }
}

// ----------------- BOOKINGS MANAGEMENT ----------------- //

async function loadAdminBookings() {
    const tableBody = document.getElementById('adminBookingsTableBody');
    if (!tableBody) return;

    const status = document.getElementById('adminBookingStatusFilter')?.value || '';
    const search = document.getElementById('adminBookingSearch')?.value || '';

    try {
        const url = new URL('/api/admin/bookings', window.location.origin);
        if (status) url.searchParams.append('status', status);
        if (search) url.searchParams.append('search', search);

        const res = await fetch(url);
        const data = await res.json();

        if (data.bookings) {
            adminBookings = data.bookings;
            renderAdminBookingsTable();
        }
    } catch (err) {
        console.error('Error loading bookings:', err);
    }
}

function renderAdminBookingsTable() {
    const tableBody = document.getElementById('adminBookingsTableBody');
    if (!tableBody) return;

    if (adminBookings.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="px-6 py-12 text-center text-slate-500">
                    <i class="fa-regular fa-calendar-xmark text-3xl mb-2 text-slate-400"></i>
                    <p class="font-medium">No appointment bookings found.</p>
                </td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = adminBookings.map(b => {
        const statusColors = {
            pending: 'bg-amber-100 text-amber-800 border-amber-200',
            confirmed: 'bg-sky-100 text-sky-800 border-sky-200',
            completed: 'bg-emerald-100 text-emerald-800 border-emerald-200',
            cancelled: 'bg-rose-100 text-rose-800 border-rose-200'
        };

        const waText = encodeURIComponent(
            `Hello ${b.patient_name}, this is Rahul Physio regarding your home visit appointment request for ${b.service_name} on ${b.preferred_date} (${b.preferred_time}).`
        );
        const waUrl = `https://wa.me/91${b.phone.replace(/\D/g, '')}?text=${waText}`;

        return `
            <tr class="hover:bg-slate-50/80 transition border-b border-slate-100">
                <td class="px-6 py-4">
                    <div class="font-bold text-slate-900 text-sm">${escapeHtml(b.patient_name)}</div>
                    <div class="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                        <i class="fa-solid fa-location-dot text-sky-600"></i> ${escapeHtml(b.area)}
                    </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <a href="tel:${b.phone}" class="text-sky-700 font-semibold text-sm hover:underline flex items-center gap-1">
                        <i class="fa-solid fa-phone text-xs"></i> ${b.phone}
                    </a>
                </td>
                <td class="px-6 py-4 text-xs">
                    <span class="font-semibold text-slate-800 block">${b.preferred_date}</span>
                    <span class="text-slate-500">${b.preferred_time}</span>
                </td>
                <td class="px-6 py-4">
                    <span class="font-semibold text-slate-800 text-xs block">${escapeHtml(b.service_name)}</span>
                    ${b.message ? `<span class="text-[11px] text-slate-500 italic block mt-0.5 line-clamp-1" title="${escapeHtml(b.message)}">"${escapeHtml(b.message)}"</span>` : ''}
                </td>
                <td class="px-6 py-4">
                    <select onchange="updateBookingStatus(${b.id}, this.value)" 
                            class="text-xs font-bold rounded-lg border px-2.5 py-1 focus:ring-1 focus:ring-sky-500 cursor-pointer ${statusColors[b.status] || 'bg-slate-100'}">
                        <option value="pending" ${b.status === 'pending' ? 'selected' : ''}>⏳ Pending</option>
                        <option value="confirmed" ${b.status === 'confirmed' ? 'selected' : ''}>✓ Confirmed</option>
                        <option value="completed" ${b.status === 'completed' ? 'selected' : ''}>★ Completed</option>
                        <option value="cancelled" ${b.status === 'cancelled' ? 'selected' : ''}>✕ Cancelled</option>
                    </select>
                </td>
                <td class="px-6 py-4 text-xs text-slate-400 whitespace-nowrap">
                    ${b.created_at ? b.created_at.split(' ')[0] : 'Recent'}
                </td>
                <td class="px-6 py-4 text-right whitespace-nowrap">
                    <div class="inline-flex items-center gap-2">
                        <a href="${waUrl}" target="_blank" 
                           class="p-2 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 rounded-lg text-xs font-semibold transition"
                           title="WhatsApp Patient">
                            <i class="fa-brands fa-whatsapp text-sm"></i>
                        </a>
                        <a href="tel:${b.phone}" 
                           class="p-2 bg-sky-50 text-sky-700 hover:bg-sky-100 rounded-lg text-xs font-semibold transition"
                           title="Call Patient">
                            <i class="fa-solid fa-phone text-xs"></i>
                        </a>
                        <button onclick="confirmDeleteBooking(${b.id})" 
                                class="p-2 bg-rose-50 text-rose-600 hover:bg-rose-100 rounded-lg text-xs font-semibold transition"
                                title="Delete Record">
                            <i class="fa-solid fa-trash-can text-xs"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

async function updateBookingStatus(bookingId, newStatus) {
    try {
        const res = await fetch(`/api/admin/bookings/${bookingId}/status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        const data = await res.json();
        if (res.ok && data.success) {
            loadDashboardStats();
            Swal.fire({
                icon: 'success',
                title: 'Status Updated',
                text: `Booking marked as ${newStatus}`,
                timer: 1200,
                showConfirmButton: false
            });
        }
    } catch (err) {
        console.error(err);
    }
}

function confirmDeleteBooking(bookingId) {
    Swal.fire({
        title: 'Delete Booking Record?',
        text: 'This will remove the appointment record permanently.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#e11d48',
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel'
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                const res = await fetch(`/api/admin/bookings/${bookingId}`, { method: 'DELETE' });
                const data = await res.json();
                if (res.ok && data.success) {
                    loadAdminBookings();
                    loadDashboardStats();
                }
            } catch (err) {
                console.error(err);
            }
        }
    });
}

// ----------------- MODALS & ACCOUNT ----------------- //

function initAdminModals() {
    const therapyForm = document.getElementById('therapyForm');
    if (therapyForm) {
        therapyForm.addEventListener('submit', handleTherapyFormSubmit);
    }

    const pwdForm = document.getElementById('changePasswordForm');
    if (pwdForm) {
        pwdForm.addEventListener('submit', handleChangePassword);
    }

    // Search and filter listeners
    const searchInput = document.getElementById('adminTherapySearch');
    if (searchInput) {
        searchInput.addEventListener('input', () => loadAdminTherapies());
    }

    const catFilter = document.getElementById('adminCategoryFilter');
    if (catFilter) {
        catFilter.addEventListener('change', () => loadAdminTherapies());
    }

    const statusFilter = document.getElementById('adminStatusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', () => loadAdminTherapies());
    }

    const bookingSearch = document.getElementById('adminBookingSearch');
    if (bookingSearch) {
        bookingSearch.addEventListener('input', () => loadAdminBookings());
    }

    const bookingStatus = document.getElementById('adminBookingStatusFilter');
    if (bookingStatus) {
        bookingStatus.addEventListener('change', () => loadAdminBookings());
    }
}

function openChangePasswordModal() {
    const modal = document.getElementById('changePasswordModal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function closeChangePasswordModal() {
    const modal = document.getElementById('changePasswordModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

async function handleChangePassword(e) {
    e.preventDefault();
    const old_password = document.getElementById('oldPasswordInput').value;
    const new_password = document.getElementById('newPasswordInput').value;
    const confirm_password = document.getElementById('confirmPasswordInput').value;

    if (new_password !== confirm_password) {
        Swal.fire('Password Mismatch', 'New passwords do not match.', 'warning');
        return;
    }

    try {
        const res = await fetch('/api/admin/change-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ old_password, new_password })
        });
        const data = await res.json();

        if (res.ok && data.success) {
            closeChangePasswordModal();
            document.getElementById('changePasswordForm').reset();
            Swal.fire({
                icon: 'success',
                title: 'Password Updated!',
                text: 'Your admin password has been changed securely.',
                timer: 1600,
                showConfirmButton: false
            });
        } else {
            Swal.fire('Error', data.error || 'Failed to change password', 'error');
        }
    } catch (err) {
        Swal.fire('Error', 'Server communication failure', 'error');
    }
}

async function handleAdminLogout() {
    try {
        await fetch('/api/admin/logout', { method: 'POST' });
        window.location.href = '/admin/login';
    } catch (err) {
        window.location.href = '/admin/login';
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
