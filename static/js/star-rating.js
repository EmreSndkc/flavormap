/**
 * FlavorMap - İnteraktif Yıldız Puanlama Widget'ı
 *
 * Sayfada `data-star-rating` özniteliği bulunan her container'ı
 * tıklanabilir 5 yıldızlı bir puanlama widget'ına dönüştürür.
 *
 * Kullanım:
 *   <div data-star-rating data-input="id_stars" data-initial="3"></div>
 *   <input type="hidden" name="stars" id="id_stars" value="3">
 */
(function () {
    'use strict';

    function buildWidget(container) {
        var inputId = container.getAttribute('data-input');
        var input = inputId ? document.getElementById(inputId) : null;
        if (!input) {
            return;
        }

        var initial = parseInt(container.getAttribute('data-initial'), 10);
        if (isNaN(initial) || initial < 1 || initial > 5) {
            initial = parseInt(input.value, 10) || 0;
        }

        // Görsel yıldızları kur
        container.innerHTML = '';
        container.classList.add('fm-star-widget');

        var stars = [];
        for (var i = 1; i <= 5; i++) {
            var star = document.createElement('span');
            star.className = 'fm-star';
            star.setAttribute('role', 'button');
            star.setAttribute('tabindex', '0');
            star.setAttribute('data-value', String(i));
            star.setAttribute('aria-label', i + ' yıldız');
            star.textContent = '\u2605'; // ★
            container.appendChild(star);
            stars.push(star);
        }

        var label = document.createElement('span');
        label.className = 'fm-star-label ms-2 text-muted';
        container.appendChild(label);

        function paint(value) {
            for (var j = 0; j < stars.length; j++) {
                if (j < value) {
                    stars[j].classList.add('active');
                } else {
                    stars[j].classList.remove('active');
                }
            }
            label.textContent = value > 0 ? (value + ' / 5') : 'Puan seçin';
        }

        function setValue(value) {
            input.value = String(value);
            paint(value);
        }

        // Olay dinleyicileri
        stars.forEach(function (star) {
            var value = parseInt(star.getAttribute('data-value'), 10);
            star.addEventListener('mouseenter', function () { paint(value); });
            star.addEventListener('click', function () { setValue(value); });
            star.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    setValue(value);
                }
            });
        });

        container.addEventListener('mouseleave', function () {
            paint(parseInt(input.value, 10) || 0);
        });

        // İlk durum
        if (initial > 0) {
            setValue(initial);
        } else {
            paint(0);
        }

        // Görsel girdiyi gizle (kullanıcı sadece widget'ı görsün)
        input.setAttribute('type', 'hidden');
    }

    document.addEventListener('DOMContentLoaded', function () {
        var containers = document.querySelectorAll('[data-star-rating]');
        for (var i = 0; i < containers.length; i++) {
            buildWidget(containers[i]);
        }
    });
})();
