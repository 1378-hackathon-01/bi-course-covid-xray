# Model card — frozen baseline

## Русский

**Архитектура.** ResNet-18 (torchvision) с инициализацией ImageNet (IMAGENET1K_V1);
при обучении заморожены все слои, кроме `layer4`, и новая голова
`Sequential(Dropout(0.5), Linear(512, 2))`. Всего 11 177 538 параметров.

**Вход / выход.** Вход — RGB-изображение 224×224×3 (Resize → ToTensor → Normalize
ImageNet). Выход — вероятности двух классов: COVID (индекс 0) и Normal (индекс 1).

**Обучение.** Adam (lr = 1e-4, weight_decay = 1e-5), `ReduceLROnPlateau(mode=max,
factor=0.5, patience=3, min_lr=1e-7)`, 20 эпох, batch 32, ранняя остановка patience = 5;
лучшая эпоха — 15-я (валидационная точность 0.9917); обучение на GPU Tesla T4 (Colab).

**Метрика на тесте** (720 снимков, 361 COVID / 359 Normal): Accuracy = **0.9833**
[Уилсон 95%: 0.9711; 0.9904]; матрица ошибок **TP 354 / FN 7 / FP 5 / TN 354**.

**Чекпойнт.** `baseline_model.pt` — PyTorch `state_dict` (122 тензора), хранится в Git LFS.
SHA-256: `0ba793cb43d0f058af66673a1026e6eef4bd898d98cae05eaf6694cb20b504f0`.

**Статус.** Модель **заморожена**: не переобучается и не изменяется ни в одной работе
цикла; используется только для инференса. Переобучение нарушило бы сопоставимость
результатов.

## English summary

ResNet-18 (ImageNet-initialised) with a Dropout(0.5) + Linear(512→2) head; only `layer4`
and the head were trained (20 epochs, Adam 1e-4, batch 32, best epoch 15, validation
accuracy 0.9917). Input: 224×224×3 RGB; output: two class probabilities (COVID / Normal).
Test accuracy: **0.9833** (Wilson 95% CI 0.9711–0.9904); confusion matrix
TP 354 / FN 7 / FP 5 / TN 354. The checkpoint is frozen and reused as-is in every stage
of the practical cycle.

## FROZEN — do not retrain

- Only load: `src/models/architecture.py::load_frozen_model`.
- Never call an optimizer on this model.
- The SHA-256 above is the integrity check; `tests/test_model_loading.py` verifies that the
  checkpoint loads into the reconstructed architecture.
