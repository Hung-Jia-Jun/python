// Just add this script to your camera. It doesn't need any configuration.

using UnityEngine;
using UnityEngine.UI;
using System;
public class TouchCamera : MonoBehaviour {
	bool PCEditor;
	void Start()
	{
		if (Application.platform == RuntimePlatform.OSXEditor) 
		{
			PCEditor = true;			
		}

	}

	public Vector3 OldPos;
	public float dragSpeed=5;
	private Vector3 dragOrigin;
	//public InputField DragSpeed;
	//public Text DragCount;
	void Update() {
		//dragSpeed = float.Parse(DragSpeed.text);
		//DragCount.text = Input.touchCount.ToString ();
		if (PCEditor) 
		{
			if (Input.GetMouseButtonDown(0))
			{
				dragOrigin = Input.mousePosition;
				return;
			}

			if (!Input.GetMouseButton (0)) 
			{
				OldPos = transform.position;
				return;

			}

			Vector3 pos = Camera.main.ScreenToViewportPoint(Input.mousePosition - dragOrigin);
			Vector3 move = new Vector3(OldPos.x-(pos.x*dragSpeed), OldPos.y,OldPos.z -(pos.y*dragSpeed));
			transform.position = move;

		}

		else 
		{
			if (Input.touchCount==2)
			{
				dragOrigin = Input.GetTouch(0).position;
				return;
			}

			if (Input.touchCount == 0) //離開螢幕了
			{
				OldPos = transform.position;
				return;

			}
			if (Input.touchCount == 2) 
			{
				Vector3 TouchNextPos = Input.GetTouch (0).position;
				Vector3 pos = Camera.main.ScreenToViewportPoint(TouchNextPos - dragOrigin);
				Vector3 move = new Vector3(OldPos.x-(pos.x*dragSpeed), OldPos.y,OldPos.z -(pos.y*dragSpeed));
				transform.position = move;

			}


		}
		}
}
