import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import iirfilter, filtfilt
import warnings


warnings.filterwarnings("ignore")


init_amplitude = 1.0
init_frequency = 1.0
init_phase = 0.0
init_noise_mean = 0.0
init_noise_cov = 0.1
init_cutoff = 2.0  


fs = 1000  
t = np.linspace(0, 10, 10 * fs, endpoint=False)


current_noise_mean = init_noise_mean
current_noise_cov = init_noise_cov
current_noise = np.random.normal(current_noise_mean, np.sqrt(current_noise_cov), len(t))

def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    """
    Генерує чисту та зашумлену гармоніку згідно з вимогами.
    Шум перераховується ТІЛЬКИ якщо змінилися його параметри.
    """
    global current_noise_mean, current_noise_cov, current_noise
    
    
    if noise_mean != current_noise_mean or noise_covariance != current_noise_cov:
        current_noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
        current_noise_mean = noise_mean
        current_noise_cov = noise_covariance
        
    
    clean_harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    
    if show_noise:
        return clean_harmonic + current_noise, clean_harmonic
    else:
        return clean_harmonic, clean_harmonic

def apply_filter(data, cutoff_freq, fs_rate):
    """
    Застосовує низькочастотний IIR фільтр для пригнічення шуму.
    Використовується filtfilt для уникнення фазового зсуву.
    """
    nyq = 0.5 * fs_rate  
    normal_cutoff = cutoff_freq / nyq
   
    b, a = iirfilter(N=4, Wn=normal_cutoff, btype='lowpass', ftype='butter')
    filtered_data = filtfilt(b, a, data)
    return filtered_data


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(left=0.15, bottom=0.45, hspace=0.35)
fig.canvas.manager.set_window_title('Лабораторна робота 4 - Візуалізація та фільтрація')


ax1.set_title("Оригінальна гармоніка (із шумом або без)")
ax1.set_xlabel("Час (с)")
ax1.set_ylabel("Амплітуда")
ax1.grid(True, linestyle='--', alpha=0.6)
noisy_sig, clean_sig = harmonic_with_noise(init_amplitude, init_frequency, init_phase, init_noise_mean, init_noise_cov, True)
line_clean1, = ax1.plot(t, clean_sig, 'g-', lw=2, label="Чиста гармоніка")
line_noisy1, = ax1.plot(t, noisy_sig, 'r-', lw=1, alpha=0.5, label="Зашумлена гармоніка")
ax1.legend(loc="upper right")


ax2.set_title("Відфільтрована гармоніка vs Чиста гармоніка")
ax2.set_xlabel("Час (с)")
ax2.set_ylabel("Амплітуда")
ax2.grid(True, linestyle='--', alpha=0.6)
filtered_sig = apply_filter(noisy_sig, init_cutoff, fs)
line_clean2, = ax2.plot(t, clean_sig, 'g-', lw=2, label="Чиста гармоніка", alpha=0.5)
line_filtered, = ax2.plot(t, filtered_sig, 'b-', lw=2, label="Відфільтрована гармоніка")
ax2.legend(loc="upper right")


axcolor = 'lightgoldenrodyellow'

ax_amp = plt.axes([0.15, 0.35, 0.65, 0.03], facecolor=axcolor)
ax_freq = plt.axes([0.15, 0.30, 0.65, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.15, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_noise_mean = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_noise_cov = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_cutoff = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)

samp = Slider(ax_amp, 'Амплітуда', 0.1, 5.0, valinit=init_amplitude)
sfreq = Slider(ax_freq, 'Частота', 0.1, 10.0, valinit=init_frequency)
sphase = Slider(ax_phase, 'Фаза', 0.0, 2*np.pi, valinit=init_phase)
snoise_mean = Slider(ax_noise_mean, 'Шум (Середнє)', -2.0, 2.0, valinit=init_noise_mean)
snoise_cov = Slider(ax_noise_cov, 'Шум (Дисперсія)', 0.01, 2.0, valinit=init_noise_cov)
scutoff = Slider(ax_cutoff, 'Зріз фільтра', 0.1, 20.0, valinit=init_cutoff)


ax_check = plt.axes([0.85, 0.25, 0.13, 0.10], facecolor=axcolor)
check = CheckButtons(ax_check, ['Показати шум'], [True])

ax_reset = plt.axes([0.85, 0.10, 0.1, 0.05])
button_reset = Button(ax_reset, 'Reset', color=axcolor, hovercolor='0.975')


def update(val):
    amp = samp.val
    freq = sfreq.val
    phase = sphase.val
    n_mean = snoise_mean.val
    n_cov = snoise_cov.val
    cutoff = scutoff.val
    
    show_noise = check.get_status()[0]
    
    
    noisy_signal, clean_signal = harmonic_with_noise(amp, freq, phase, n_mean, n_cov, show_noise)
    
    
    if show_noise:
        line_noisy1.set_ydata(noisy_signal)
        line_noisy1.set_visible(True)
    else:
        line_noisy1.set_visible(False)
        
    line_clean1.set_ydata(clean_signal)
    
   
    actual_noisy_signal = clean_signal + current_noise
    filtered_signal = apply_filter(actual_noisy_signal, cutoff, fs)
    
    line_clean2.set_ydata(clean_signal)
    line_filtered.set_ydata(filtered_signal)
    
    
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    
    fig.canvas.draw_idle()


samp.on_changed(update)
sfreq.on_changed(update)
sphase.on_changed(update)
snoise_mean.on_changed(update)
snoise_cov.on_changed(update)
scutoff.on_changed(update)
check.on_clicked(update)

def reset(event):
    """Скидає всі віджети до початкових значень"""
    samp.reset()
    sfreq.reset()
    sphase.reset()
    snoise_mean.reset()
    snoise_cov.reset()
    scutoff.reset()
    
    if not check.get_status()[0]:
        check.set_active(0)

button_reset.on_clicked(reset)


fig.text(0.02, 0.02, "Інструкція:\nЗмінюйте параметри слайдерами.\nКнопка Reset повертає початкові налаштування.", fontsize=9, color='gray')

plt.show()