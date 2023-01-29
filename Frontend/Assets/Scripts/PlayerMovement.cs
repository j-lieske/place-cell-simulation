using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using PathCreation;

public class PlayerMovement : MonoBehaviour
{
    public PathCreator pathCreator;
    public float speed = 5;
    public bool disabled = false;
    float distanceTravelled;
    int keyPressed;

    private void Start () {
        keyPressed = 0;
    }

    // Update is called once per frame
    void Update()
    {   
        if(!disabled)
        {
            if (Input.GetKeyDown(KeyCode.W) && keyPressed == 0) keyPressed = 1;
            if (Input.GetKeyDown(KeyCode.S) && keyPressed == 0) keyPressed = 2;
            if (Input.GetKeyUp(KeyCode.W) && keyPressed == 1) keyPressed = 0;
            if (Input.GetKeyUp(KeyCode.S) && keyPressed == 2) keyPressed = 0;

            Vector3 facingDirection = transform.forward;
            Vector3 pathDirection = pathCreator.path.GetDirectionAtDistance(distanceTravelled);

            if ((facingDirection + pathDirection).magnitude > (facingDirection - pathDirection).magnitude)
            {
                //Player is facing the same way as the path
                if (keyPressed == 1) distanceTravelled += speed * Time.deltaTime;
                if (keyPressed == 2) distanceTravelled -= speed * Time.deltaTime;
            }
            else
            {
                //Player is facing the opposite way from the path
                if (keyPressed == 1) distanceTravelled -= speed * Time.deltaTime;
                if (keyPressed == 2) distanceTravelled += speed * Time.deltaTime;
            }
            transform.position = pathCreator.path.GetPointAtDistance(distanceTravelled);
        }
    }

    public void setPos(float pos)
    {
        distanceTravelled = pos;
        transform.position = pathCreator.path.GetPointAtDistance(distanceTravelled);
    }

    public Vector3 getPos() {
        return pathCreator.path.GetPointAtDistance(distanceTravelled);
    }
}
