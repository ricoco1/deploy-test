document.getElementById('others').addEventListener('change', function() {
    var othersDetails = document.getElementById('othersDetails');
    var othersText = document.getElementById('othersText');
    if (this.checked) {
        othersDetails.classList.remove('hidden');
        othersText.setAttribute('required', 'required');
    } else {
        othersDetails.classList.add('hidden');
        othersText.removeAttribute('required');
    }
});

document.getElementById('bookForOthers').addEventListener('change', function() {
    var guestNameField = document.getElementById('guestNameField');
    guestNameField.classList.remove('hidden');
    document.getElementById('guestName').setAttribute('required', 'required');
});

document.getElementById('sameAsBooker').addEventListener('change', function() {
    var guestNameField = document.getElementById('guestNameField');
    guestNameField.classList.add('hidden');
    document.getElementById('guestName').removeAttribute('required');
});

document.getElementById('lamaInap').addEventListener('change', function() {
    var lamaInap = parseInt(this.value);
    var hargaPerMalam = {{harga_diskon}}; // Anda dapat menggantinya dengan harga dari database jika dinamis
    var pajakBiaya = (hargaPerMalam * lamaInap * 0.1) + 15000;
    var hargaKamar = hargaPerMalam * lamaInap;
    var hargaTotal = hargaKamar;

    document.getElementById('hargaKamar').innerText = 'Rp ' + hargaKamar.toLocaleString('id-ID');
    document.getElementById('hargaTotal').innerText = 'Rp ' + hargaTotal.toLocaleString('id-ID');
});

document.getElementById('pay-button').addEventListener('click', function(e) {
    e.preventDefault();

    var data = {
        namaLengkap: document.getElementById('namaLengkap').value,
        email: document.getElementById('email').value,
        nomorHandphone: document.getElementById('nomorHandphone').value,
    };

    fetch('/get_token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            console.log('Received token:', data.token);
            snap.pay(data.token);
        } else {
            console.error('Error:', data.error);
            alert('Failed to get token: ' + JSON.stringify(data.error));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to get token: ' + error.message);
    });
});
document.getElementById('lamaInap').addEventListener('change', function() {
    var lamaInap = parseInt(this.value);
    var hargaPerMalam = {{harga_diskon}};
    var hargaKamar = hargaPerMalam * lamaInap;
    var hargaTotal = hargaKamar;

    document.getElementById('hargaKamar').innerText = 'Rp ' + hargaKamar.toLocaleString('id-ID');
    document.getElementById('hargaTotal').innerText = 'Rp ' + hargaTotal.toLocaleString('id-ID');

    var checkInDate = new Date('{{ check_in_date }}');
    checkInDate.setDate(checkInDate.getDate() + lamaInap);
    var options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
    var checkOutDateStr = checkInDate.toLocaleDateString('id-ID', options) + ' Sebelum 12:00';
    document.getElementById('checkOutDate').innerText = 'Check-out: ' + checkOutDateStr;
});

document.addEventListener('DOMContentLoaded', function() {
    var hargaNormal = {{ harga_normal }};
    var hargaDiskon = {{ harga_diskon }};

    document.querySelector('.discounted-price').innerText = 'Rp ' + hargaNormal.toLocaleString('id-ID');
    document.querySelector('.total-price').innerText = 'Rp ' + hargaDiskon.toLocaleString('id-ID');
    document.querySelector('#hargaKamar').innerText = 'Rp ' + hargaDiskon.toLocaleString('id-ID');
    document.querySelector('#hargaTotal').innerText = 'Rp ' + hargaDiskon.toLocaleString('id-ID');
});