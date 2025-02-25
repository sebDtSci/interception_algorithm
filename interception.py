# interception.py
import numpy as np

def predict_interception(target_pos, target_vel, interceptor_pos, interceptor_speed):
    """
    Prédit le point d'interception en supposant un mouvement linéaire de la cible.
    
    :param target_pos: Position actuelle de la cible (x, y)
    :param target_vel: Vitesse de la cible (vx, vy)
    :param interceptor_pos: Position actuelle de l'intercepteur (x, y)
    :param interceptor_speed: Vitesse de l'intercepteur
    :return: Coordonnées du point d'interception (x, y)
    """
    target_pos = np.array(target_pos, dtype=np.float64)
    target_vel = np.array(target_vel, dtype=np.float64)
    interceptor_pos = np.array(interceptor_pos, dtype=np.float64)
    
    # Résolution de l'équation quadratique pour le temps d'interception
    relative_pos = target_pos - interceptor_pos
    a = np.dot(target_vel, target_vel) - interceptor_speed**2
    b = 2 * np.dot(relative_pos, target_vel)
    c = np.dot(relative_pos, relative_pos)

    delta = b**2 - 4 * a * c
    if delta < 0:
        return None  # Pas de solution, trop lent pour intercepter

    sqrt_delta = np.sqrt(delta)
    t1 = (-b + sqrt_delta) / (2 * a)
    t2 = (-b - sqrt_delta) / (2 * a)

    # On prend le temps d'interception positif et minimal
    t = max(t1, t2)
    if t < 0:
        return None

    return target_pos + target_vel * t  # Position estimée de l'interception