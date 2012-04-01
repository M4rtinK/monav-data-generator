import QtQuick 1.1
import com.nokia.meego 1.0
import "uiconstants.js" as UI
import "functions.js" as F

Page {
    id: tabMap
    property int buttonSize: 72

    function showOnMap(lat, lon) {
        pinchmap.setCenterLatLon(lat, lon);
        tabGroup.currentTab = tabMap
    }

    property bool center : true

    Component.onCompleted : {
        pinchmap.setCenterLatLon(gps.lastGoodFix.lat, gps.lastGoodFix.lon);
    }

    PinchMap {
        id: pinchmap
        width: parent.width
        height: parent.height
        zoomLevel: 11

        Connections {
            target: gps
            onLastGoodFixChanged: {
                //console.log("fix changed")
                if (tabMap.center && ! updateTimer.running) {
                    //console.debug("Update from GPS position")
                    pinchmap.setCenterLatLon(gps.lastGoodFix.lat, gps.lastGoodFix.lon);
                    updateTimer.start();
                } else if (tabMap.center) {
                    console.debug("Update timer preventing another update.");
                }
            }
        }

        onDrag : {
            // disable map centering once drag is detected
            tabMap.center = false
        }

        Timer {
            id: updateTimer
            interval: 500
            repeat: false
        }

        /*
        onLatitudeChanged: {
            settings.mapPositionLat = latitude;
        }
        onLongitudeChanged: {
            settings.mapPositionLon = longitude;
        }
        onZoomLevelChanged: {
            settings.mapZoom = pinchmap.zoomLevel;
        }
        */

        // Rotating the map for fun and profit.
        // angle: -compass.azimuth
        showCurrentPosition: true
        currentPositionValid: gps.hasFix
        currentPositionLat: gps.lastGoodFix.lat
        currentPositionLon: gps.lastGoodFix.lon
        //currentPositionAzimuth: compass.azimuth
        //TODO: switching between GPS bearing & compass azimuth
        currentPositionAzimuth: gps.lastGoodFix.bearing
        currentPositionError: gps.lastGoodFix.error

    }

    Image {
        id: compassImage
        /* TODO: investigate how to replace this by an image loader
         what about rendered size ?
         */
        source: "../../../../themes/"+ rWin.theme +"/windrose-simple.svg"
        transform: [Rotation {
                id: azCompass
                origin.x: compassImage.width/2
                origin.y: compassImage.height/2
                //angle: -compass.azimuth
            }]
        anchors.left: tabMap.left
        anchors.leftMargin: 16
        anchors.top: tabMap.top
        anchors.topMargin: 16
        smooth: true
        width: Math.min(tabMap.width/4, tabMap.height/4)
        fillMode: Image.PreserveAspectFit
        z: 2

        Image {
            property int angle: gps.targetBearing || 0
            property int outerMargin: 0
            id: arrowImage
            //visible: (gps.targetValid && gps.lastGoodFix.valid)
            /* TODO: investigate how to replace this by an image loader
             what about rendered size ?
             */
            source: "../../../../themes/"+ rWin.theme +"/arrow_target.svg"
            width: (compassImage.paintedWidth / compassImage.sourceSize.width)*sourceSize.width
            fillMode: Image.PreserveAspectFit
            x: compassImage.width/2 - width/2
            y: arrowImage.outerMargin
            z: 3
            transform: Rotation {
                origin.y: compassImage.height/2 - arrowImage.outerMargin
                origin.x: arrowImage.width/2
                angle: arrowImage.angle
            }
        }
    }

    /*
    Text {
        text: F.formatDistance(gps.targetDistance || 0, settings)
        anchors.horizontalCenter: compassImage.horizontalCenter
        anchors.top: compassImage.bottom
        anchors.topMargin: 8
        style: Text.Outline
        styleColor: "white"
        font.pixelSize: 32
        visible: (gps.targetValid && gps.data.valid && gps.targetDistanceValid)
    }
    */

    Row {
        id: buttonsRight
        anchors.bottom: pinchmap.bottom
        anchors.bottomMargin: 16
        anchors.right: pinchmap.right
        anchors.rightMargin: 16
        spacing: 16
        Button {
            //iconSource: "image://theme/icon-m-input-add"
            iconSource: "image://theme/icon-m-common-add"
            onClicked: {pinchmap.zoomIn() }
            width: parent.parent.buttonSize
            height: parent.parent.buttonSize
            enabled : pinchmap.zoomLevel != pinchmap.maxZoomLevel
        }
        Button {
            //iconSource: "image://theme/icon-m-input-remove"
            iconSource: "image://theme/icon-m-common-remove"
            onClicked: {pinchmap.zoomOut() }
            width: parent.parent.buttonSize
            height: parent.parent.buttonSize
            enabled : pinchmap.zoomLevel != pinchmap.minZoomLevel
        }
    }
    Column {
        id: buttonsLeft
        anchors.bottom: pinchmap.bottom
        anchors.bottomMargin: 16
        anchors.left: pinchmap.left
        anchors.leftMargin: 16
        spacing: 16
        Button {
            //iconSource: "image://theme/icon-m-image-edit-resize"
            //iconSource: "image://theme/icon-m-toolbar-tab-next"
            iconSource: "image://theme/icon-m-transfer-download"
            rotation : 180
            checkable : true
            onClicked: {
                platform.toggleFullscreen()
            }
            width: parent.parent.buttonSize
            height: parent.parent.buttonSize
        }
        Button {
            id: followPositionButton
            iconSource: "image://theme/icon-m-common-location"
            width: parent.parent.buttonSize
            height: parent.parent.buttonSize
            checked : tabMap.center
            /*
            checked is bound to tabMap.center, no need to toggle
            it's value when the button is pressed
            */
            checkable: false
            onClicked: {
                // toggle map centering
                if (tabMap.center) {
                    tabMap.center = false // disable
                } else {
                    tabMap.center = true // enable
                    if (gps.lastGoodFix) { // recenter at once
                        pinchmap.setCenterLatLon(gps.lastGoodFix.lat, gps.lastGoodFix.lon);
                    }
                }
            }
        }
        Button {
            id: mainMenuButton
            iconSource: "image://theme/icon-m-content-application"
            width: parent.parent.buttonSize
            height: parent.parent.buttonSize
            onClicked: {
                rWin.pageStack.push(mainMenu)
            }
        }
    }
    ProgressBar {
        id: zoomBar
        anchors.top: pinchmap.top;
        anchors.topMargin: 1
        anchors.left: pinchmap.left;
        anchors.right: pinchmap.right;
        maximumValue: pinchmap.maxZoomLevel;
        minimumValue: pinchmap.minZoomLevel;
        value: pinchmap.zoomLevel;
        visible: false
        Behavior on value {
            SequentialAnimation {
                PropertyAction { target: zoomBar; property: "visible"; value: true }
                NumberAnimation { duration: 100; }
                PauseAnimation { duration: 750; }
                PropertyAction { target: zoomBar; property: "visible"; value: false }
            }
        }
    }
}