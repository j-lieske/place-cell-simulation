using System;
using System.Collections;
using System.Collections.Generic;
using NetMQ;
using UnityEngine;

public class BackendClient : MonoBehaviour
{
    private BackendRequester backendRequester;

    // Start is called before the first frame update
    void Start()
    {
        InitializeServer();
    }

    public void InitializeServer()
    {
        backendRequester = new BackendRequester();
        backendRequester.Start();
    }

    public void Categorize(int[]input, Action<int[]> onOutputReceived, Action<Exception> fallback)
    {
        backendRequester.SetOnTextReceivedListener(onOutputReceived, fallback);
        backendRequester.SendInput(input);
    }
}
