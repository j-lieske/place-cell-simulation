using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

public class SomManager : MonoBehaviour
{
    public Camera cam;
    public BackendClient client;
    public PlayerMovement player;
    public GameObject unitPrefab;

    public Image[] cells;
    private Image lastActiveCell;
    private Image activeCell;

    public Material[] mats;
    private bool placeUnit;
    private Material currentMat;

    // Start is called before the first frame update
    void Start()
    {
        foreach(Image cell in cells){
            cell.color = new Color(0.3f, 0.3f, 0.3f, 0.8f);
        }
        InvokeRepeating("CategorizeImage", 0.3f, 0.3f);
    }

    private void Update () {
        if(lastActiveCell != activeCell){
            if(lastActiveCell != null) {
                lastActiveCell.color = new Color(0.5f, 0.5f, 0.5f, 0.5f);
            }
            activeCell.color = new Color(1f, 1f, 1f, 1f);
        }
        if(placeUnit){
            placeUnit = false;
            GameObject obj = Instantiate(unitPrefab, player.getPos(), Quaternion.identity);
            obj.GetComponent<MeshRenderer>().material = currentMat;
        }
    }

    void CategorizeImage()  
    {
        RenderTexture screenTexture = new RenderTexture(Screen.width, Screen.height, 0);
        cam.targetTexture = screenTexture;
        RenderTexture.active = screenTexture;
        cam.Render();
        Texture2D screenImage = new Texture2D(cam.pixelWidth, cam.pixelHeight);
        screenImage.ReadPixels(new Rect(0, Screen.height- cam.pixelHeight, cam.pixelWidth, cam.pixelHeight), 0, 0);
        screenImage.Apply();
        cam.targetTexture = null;
        RenderTexture.active = null;
        Destroy(screenTexture);
        int[] pxlArray = screenImage.GetPixelData<int>(0).ToArray();
        Destroy(screenImage);
        pxlArray = pxlArray.Concat(new int[] { cam.pixelWidth, cam.pixelHeight }).ToArray();
        client.Categorize(pxlArray, output => {
            lastActiveCell = activeCell;
            activeCell = cells[output[0] * 3 + output[1]];
            placeUnit = true;
            currentMat = mats[output[0] * 3 + output[1]];
        }, error => { });
    }
}
