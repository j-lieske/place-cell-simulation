using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    public float mouseSensitivity = 100f;
    public Transform playerBody;
    //float xRotation = 0f;
    public bool disabled = false;
    private Camera mainCam;
    private bool altView;

    private void Start () {
        Cursor.lockState = CursorLockMode.Locked;
        mainCam = GetComponent<Camera>();
        altView = false;
    }

    // Update is called once per frame
    void Update()
    {
        if (!disabled)
        {
            //Camera Rotation
            float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity;
            //float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity;

            //xRotation -= mouseY;
            //xRotation = Mathf.Clamp(xRotation, -45f, 45f);

            //transform.localRotation = Quaternion.Euler(xRotation, 0f, 0f);
            playerBody.Rotate(Vector3.up * mouseX);
        }

        if(Input.GetKeyDown(KeyCode.C)){
            if(!altView){
                mainCam.rect = new Rect(0f, 0f, 0.5f, 0.5f);
            } else {
                mainCam.rect = new Rect(0f, 0f, 1f, 1f);
            }
            altView = !altView;
        }
    }

    public void SetCameraAngle(float degree)
    {
        playerBody.localRotation = Quaternion.Euler(0f, degree, 0f);
    }
}
