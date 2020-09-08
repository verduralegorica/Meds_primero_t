# Experimento_meds_parte I (T)

El proyecto consta de 3 aplicaciones: (i) meds_primero/**meds_primero_t**, (ii) meds_segundo y (iii) meds_tercero.

Para la primera parte, existen 2 aplicaciones: meds_primero (control) y meds_primero_t (tratamiento).

La configuración (en settings) variará ligeramente por eso. Este aplicativo (meds_primero_t) refiere al de tratamiento, por tanto la config es la siguiente:

- SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=5)
- SESSION_CONFIGS = [dict(name='exp_meds_gt', display_name='Exp_meds_tratamiento', num_demo_participants=1, app_sequence=['MobilePhones', 'meds_primero_t', 'meds_segundo', 'meds_tercero'])]


Esta aplicación contiene lo siguiente:
1. Instrucciones
2. Template de contacto y botón de instrucciones
3. Preguntas de entendimiento de instrucciones con opciones aleatorias
4. Cartilla de información de medicamentos

