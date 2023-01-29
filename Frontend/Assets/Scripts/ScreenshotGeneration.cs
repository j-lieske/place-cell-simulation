using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScreenshotGeneration : MonoBehaviour
{

    private string path;
    public PlayerMovement playerMove;
    public CameraController cameraControl;
    public int noOfScreenshots;

    private void Start ()
    {
        path = Application.dataPath + "\\Screenshots\\Testing\\Images\\";
    }

    private void Update ()
    {

        if (Input.GetKeyDown(KeyCode.N))
        {
            StartCoroutine(ScreenshotCoroutine());
        }
    }

    IEnumerator ScreenshotCoroutine () {
        Debug.Log("Started screenshot generation at: " + Time.time);

        playerMove.disabled = true;
        cameraControl.disabled = true;

        float pathLength = playerMove.pathCreator.path.length;
        for (int i = 0; i < noOfScreenshots; i++)
        {
            //Set random position and camera angle
            playerMove.setPos(Random.Range(0f, pathLength));
            cameraControl.SetCameraAngle(Random.Range(0f, 360f));
            yield return null;
            TakeScreenshot();
        }

        playerMove.disabled = false;
        cameraControl.disabled = false;

        Debug.Log("Ended screenshot generation at: " + Time.time);
    }

    private void TakeScreenshot()
    {
        string imagePath = path;
        imagePath += "screenshot";
        imagePath += System.Guid.NewGuid().ToString() + ".png";

        ScreenCapture.CaptureScreenshot(imagePath, 1);
        Debug.Log("Saved Screenshot to: " + imagePath);
    }
}
